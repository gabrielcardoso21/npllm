"""
PostgreSQL + pgvector storage
Stores feedback and context with semantic search
"""

from typing import List, Dict, Any, Optional
import numpy as np
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import execute_values
import psycopg2
from pgvector.psycopg2 import register_vector

from src.utils.config import get_config
from src.utils.logging import get_logger


class PostgreSQLStorage:
    """
    Interface para PostgreSQL + pgvector
    Armazena feedback e contexto com busca semântica
    Otimizado para baixo uso de memória
    """
    
    def __init__(self):
        """Inicializa conexão com PostgreSQL"""
        self.logger = get_logger(self.__class__.__name__)
        self.config = get_config()
        db_config = self.config.database
        
        self.connection_params = {
            "host": db_config.host,
            "port": db_config.port,
            "database": db_config.database,
            "user": db_config.user,
            "password": db_config.password
        }
        
        # Pool de conexões
        self.pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=db_config.pool_size,
            **self.connection_params
        )
        
        # Inicializa schema
        conn = self.pool.getconn()
        try:
            register_vector(conn)
            self._initialize_schema(conn)
        finally:
            self.pool.putconn(conn)
        
        self.logger.info("PostgreSQL storage initialized")
    
    def _initialize_schema(self, conn):
        """Inicializa schema do banco de dados"""
        cursor = conn.cursor()
        
        # Tabela de feedback
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                score FLOAT NOT NULL,
                implicit_score FLOAT,
                emotional_score FLOAT,
                context TEXT,
                embedding vector(384),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Índice para busca semântica
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS feedback_embedding_idx
            ON feedback
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """)
        
        # Índice para score (filtragem)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS feedback_score_idx
            ON feedback (score)
        """)
        
        # Índice para contexto
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS feedback_context_idx
            ON feedback (context)
        """)
        
        # Tabela de exemplos importantes (para replay)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS important_examples (
                id SERIAL PRIMARY KEY,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                score FLOAT NOT NULL,
                context TEXT,
                embedding vector(384),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Índice para exemplos importantes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS important_examples_embedding_idx
            ON important_examples
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """)
        
        conn.commit()
        cursor.close()
        self.logger.info("Database schema initialized")
    
    def store_feedback(
        self,
        prompt: str,
        response: str,
        score: float,
        implicit_score: Optional[float] = None,
        emotional_score: Optional[float] = None,
        context: Optional[str] = None,
        embedding: Optional[np.ndarray] = None
    ) -> int:
        """
        Armazena feedback no banco
        
        Args:
            prompt: Prompt original
            response: Resposta gerada
            score: Score total (0.7 * implícito + 0.3 * emocional)
            implicit_score: Score implícito
            emotional_score: Score emocional
            context: Contexto (ex: 'python', 'odoo')
            embedding: Embedding vetorial (opcional)
        
        Returns:
            ID do feedback armazenado
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (prompt, response, score, implicit_score, emotional_score, context, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (prompt, response, score, implicit_score, emotional_score, context, embedding))
            
            feedback_id = cursor.fetchone()[0]
            conn.commit()
            
            self.logger.debug(f"Feedback stored with ID: {feedback_id}")
            return feedback_id
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error storing feedback: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_all_feedbacks(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os feedbacks
        
        Returns:
            Lista de feedbacks
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, prompt, response, score, implicit_score, emotional_score, context, created_at
                FROM feedback
                ORDER BY created_at DESC
            """)
            
            feedbacks = []
            for row in cursor.fetchall():
                feedbacks.append({
                    "id": row[0],
                    "prompt": row[1],
                    "response": row[2],
                    "score": row[3],
                    "implicit_score": row[4],
                    "emotional_score": row[5],
                    "context": row[6],
                    "created_at": row[7]
                })
            
            return feedbacks
        
        except Exception as e:
            self.logger.error(f"Error getting feedbacks: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_important_examples(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retorna exemplos importantes para replay
        
        Args:
            limit: Número máximo de exemplos
        
        Returns:
            Lista de exemplos importantes
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, prompt, response, score, context, created_at
                FROM important_examples
                ORDER BY score DESC, created_at DESC
                LIMIT %s
            """, (limit,))
            
            examples = []
            for row in cursor.fetchall():
                examples.append({
                    "id": row[0],
                    "prompt": row[1],
                    "response": row[2],
                    "score": row[3],
                    "context": row[4],
                    "created_at": row[5]
                })
            
            return examples
        
        except Exception as e:
            self.logger.error(f"Error getting important examples: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def add_important_example(
        self,
        prompt: str,
        response: str,
        score: float,
        context: Optional[str] = None,
        embedding: Optional[np.ndarray] = None
    ):
        """
        Adiciona exemplo importante para replay
        
        Args:
            prompt: Prompt original
            response: Resposta gerada
            score: Score do exemplo
            context: Contexto
            embedding: Embedding vetorial
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO important_examples (prompt, response, score, context, embedding)
                VALUES (%s, %s, %s, %s, %s)
            """, (prompt, response, score, context, embedding))
            
            conn.commit()
            self.logger.debug("Important example added")
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error adding important example: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def search_similar(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        context: Optional[str] = None,
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Busca feedbacks similares por embedding
        
        Args:
            query_embedding: Embedding da query
            top_k: Número de resultados
            context: Filtrar por contexto (opcional)
            min_score: Score mínimo
        
        Returns:
            Lista de feedbacks similares
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            
            if context:
                cursor.execute("""
                    SELECT id, prompt, response, score, context,
                           1 - (embedding <=> %s::vector) as similarity
                    FROM feedback
                    WHERE context = %s AND score >= %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """, (query_embedding.tolist(), context, min_score, query_embedding.tolist(), top_k))
            else:
                cursor.execute("""
                    SELECT id, prompt, response, score, context,
                           1 - (embedding <=> %s::vector) as similarity
                    FROM feedback
                    WHERE score >= %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """, (query_embedding.tolist(), min_score, query_embedding.tolist(), top_k))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "prompt": row[1],
                    "response": row[2],
                    "score": row[3],
                    "context": row[4],
                    "similarity": float(row[5])
                })
            
            return results
        
        except Exception as e:
            self.logger.error(f"Error searching similar: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def close(self):
        """Fecha pool de conexões"""
        if hasattr(self, 'pool'):
            self.pool.closeall()
            self.logger.info("PostgreSQL storage closed")

