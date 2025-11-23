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
        
        # Tabela de cursos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                source_type VARCHAR(50) NOT NULL,
                source_path TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'not_started',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de conteúdo de cursos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course_content (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                title VARCHAR(500),
                content TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                metadata JSONB,
                embedding vector(384),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Índice para busca semântica de conteúdo
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS course_content_embedding_idx
            ON course_content
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """)
        
        # Índice para course_id
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS course_content_course_id_idx
            ON course_content (course_id)
        """)
        
        # Tabela de conceitos aprendidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_concepts (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                concept_name VARCHAR(255) NOT NULL,
                description TEXT,
                examples JSONB,
                patterns JSONB,
                confidence FLOAT DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Índice para course_id em conceitos
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS learned_concepts_course_id_idx
            ON learned_concepts (course_id)
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
    
    def store_course(
        self,
        name: str,
        description: str,
        source_type: str,
        source_path: str
    ) -> int:
        """
        Armazena um novo curso
        
        Args:
            name: Nome do curso
            description: Descrição do curso
            source_type: Tipo de fonte ('url', 'file', 'directory', 'text')
            source_path: Caminho/URL da fonte
        
        Returns:
            ID do curso criado
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO courses (name, description, source_type, source_path)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, description, source_type, source_path))
            
            course_id = cursor.fetchone()[0]
            conn.commit()
            
            self.logger.debug(f"Course stored with ID: {course_id}")
            return course_id
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error storing course: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_course(self, course_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém um curso por ID
        
        Args:
            course_id: ID do curso
        
        Returns:
            Dicionário com informações do curso ou None
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, description, source_type, source_path, status, created_at, updated_at
                FROM courses
                WHERE id = %s
            """, (course_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Converter datetime para string ISO
            created_at = row[6]
            if hasattr(created_at, 'isoformat'):
                created_at = created_at.isoformat()
            updated_at = row[7] if row[7] else None
            if updated_at and hasattr(updated_at, 'isoformat'):
                updated_at = updated_at.isoformat()
            
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "source_type": row[3],
                "source_path": row[4],
                "status": row[5],
                "created_at": created_at,
                "updated_at": updated_at
            }
        
        except Exception as e:
            self.logger.error(f"Error getting course: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_all_courses(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os cursos
        
        Returns:
            Lista de cursos
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, description, source_type, source_path, status, created_at, updated_at
                FROM courses
                ORDER BY created_at DESC
            """)
            
            courses = []
            for row in cursor.fetchall():
                # Converter datetime para string ISO
                created_at = row[6]
                if hasattr(created_at, 'isoformat'):
                    created_at = created_at.isoformat()
                updated_at = row[7] if row[7] else None
                if updated_at and hasattr(updated_at, 'isoformat'):
                    updated_at = updated_at.isoformat()
                
                courses.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "source_type": row[3],
                    "source_path": row[4],
                    "status": row[5],
                    "created_at": created_at,
                    "updated_at": updated_at
                })
            
            return courses
        
        except Exception as e:
            self.logger.error(f"Error getting all courses: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def update_course_status(self, course_id: int, status: str):
        """
        Atualiza status de um curso
        
        Args:
            course_id: ID do curso
            status: Novo status
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE courses
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (status, course_id))
            
            conn.commit()
            self.logger.debug(f"Course {course_id} status updated to {status}")
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error updating course status: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def store_course_content(
        self,
        course_id: int,
        title: str,
        content: str,
        chunk_index: int,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[np.ndarray] = None
    ) -> int:
        """
        Armazena conteúdo de um curso
        
        Args:
            course_id: ID do curso
            title: Título do chunk
            content: Conteúdo do chunk
            chunk_index: Índice do chunk
            metadata: Metadados adicionais (JSON)
            embedding: Embedding vetorial
        
        Returns:
            ID do conteúdo armazenado
        """
        import json
        
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute("""
                INSERT INTO course_content (course_id, title, content, chunk_index, metadata, embedding)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (course_id, title, content, chunk_index, metadata_json, embedding))
            
            content_id = cursor.fetchone()[0]
            conn.commit()
            
            self.logger.debug(f"Course content stored with ID: {content_id}")
            return content_id
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error storing course content: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_course_content(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Obtém todo o conteúdo de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Lista de chunks de conteúdo
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, content, chunk_index, metadata, created_at
                FROM course_content
                WHERE course_id = %s
                ORDER BY chunk_index ASC
            """, (course_id,))
            
            content = []
            for row in cursor.fetchall():
                import json
                # Metadata pode já ser dict (se veio de processamento) ou string JSON
                if row[4]:
                    if isinstance(row[4], dict):
                        metadata = row[4]
                    else:
                        metadata = json.loads(row[4])
                else:
                    metadata = None
                content.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "chunk_index": row[3],
                    "metadata": metadata,
                    "created_at": row[5]
                })
            
            return content
        
        except Exception as e:
            self.logger.error(f"Error getting course content: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_course_content_count(self, course_id: int) -> int:
        """
        Conta número de chunks de conteúdo de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Número de chunks
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM course_content
                WHERE course_id = %s
            """, (course_id,))
            
            return cursor.fetchone()[0]
        
        except Exception as e:
            self.logger.error(f"Error counting course content: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def search_course_content(
        self,
        course_id: int,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Busca conteúdo de curso por similaridade semântica
        
        Args:
            course_id: ID do curso
            query_embedding: Embedding da query
            top_k: Número de resultados
        
        Returns:
            Lista de chunks similares
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, content, chunk_index, metadata,
                       1 - (embedding <=> %s::vector) as similarity
                FROM course_content
                WHERE course_id = %s AND embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding.tolist(), course_id, query_embedding.tolist(), top_k))
            
            results = []
            for row in cursor.fetchall():
                import json
                # Metadata pode já ser dict (se veio de processamento) ou string JSON
                if row[4]:
                    if isinstance(row[4], (dict, list)):
                        metadata = row[4]
                    else:
                        metadata = json.loads(row[4])
                else:
                    metadata = None
                results.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "chunk_index": row[3],
                    "metadata": metadata,
                    "similarity": float(row[5])
                })
            
            return results
        
        except Exception as e:
            self.logger.error(f"Error searching course content: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def store_learned_concept(
        self,
        course_id: int,
        concept_name: str,
        description: str,
        examples: Optional[List[Dict[str, Any]]] = None,
        patterns: Optional[List[Dict[str, Any]]] = None,
        confidence: float = 0.5
    ) -> int:
        """
        Armazena um conceito aprendido de um curso
        
        Args:
            course_id: ID do curso
            concept_name: Nome do conceito
            description: Descrição do conceito
            examples: Lista de exemplos
            patterns: Lista de padrões
            confidence: Confiança no conceito (0.0 a 1.0)
        
        Returns:
            ID do conceito armazenado
        """
        import json
        
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            examples_json = json.dumps(examples) if examples else None
            patterns_json = json.dumps(patterns) if patterns else None
            
            cursor.execute("""
                INSERT INTO learned_concepts (course_id, concept_name, description, examples, patterns, confidence)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (course_id, concept_name, description, examples_json, patterns_json, confidence))
            
            concept_id = cursor.fetchone()[0]
            conn.commit()
            
            self.logger.debug(f"Learned concept stored with ID: {concept_id}")
            return concept_id
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error storing learned concept: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_learned_concepts(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Obtém todos os conceitos aprendidos de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Lista de conceitos aprendidos
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, concept_name, description, examples, patterns, confidence, created_at
                FROM learned_concepts
                WHERE course_id = %s
                ORDER BY confidence DESC, created_at DESC
            """, (course_id,))
            
            concepts = []
            for row in cursor.fetchall():
                import json
                # Examples e patterns podem já ser list/dict (psycopg2 retorna JSON como Python types) ou string JSON
                if row[3]:
                    if isinstance(row[3], (dict, list)):
                        examples = row[3]
                    else:
                        examples = json.loads(row[3])
                else:
                    examples = None
                
                if row[4]:
                    if isinstance(row[4], (dict, list)):
                        patterns = row[4]
                    else:
                        patterns = json.loads(row[4])
                else:
                    patterns = None
                
                concepts.append({
                    "id": row[0],
                    "concept_name": row[1],
                    "description": row[2],
                    "examples": examples,
                    "patterns": patterns,
                    "confidence": row[5],
                    "created_at": row[6]
                })
            
            return concepts
        
        except Exception as e:
            self.logger.error(f"Error getting learned concepts: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_learned_concepts_count(self, course_id: int) -> int:
        """
        Conta número de conceitos aprendidos de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Número de conceitos
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM learned_concepts
                WHERE course_id = %s
            """, (course_id,))
            
            return cursor.fetchone()[0]
        
        except Exception as e:
            self.logger.error(f"Error counting learned concepts: {e}")
            raise
        
        finally:
            cursor.close()
            self.pool.putconn(conn)
    
    def get_course_examples_for_replay(
        self,
        course_id: int,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Obtém exemplos de um curso para uso no replay buffer
        
        Args:
            course_id: ID do curso
            limit: Número máximo de exemplos
        
        Returns:
            Lista de exemplos formatados para replay
        """
        concepts = self.get_learned_concepts(course_id)
        examples = []
        
        for concept in concepts[:limit]:
            if concept.get("examples"):
                for example in concept["examples"]:
                    examples.append({
                        "prompt": example.get("prompt", ""),
                        "response": example.get("response", ""),
                        "score": concept.get("confidence", 0.5),
                        "context": f"course_{course_id}"
                    })
        
        return examples
    
    def close(self):
        """Fecha pool de conexões"""
        if hasattr(self, 'pool'):
            self.pool.closeall()
            self.logger.info("PostgreSQL storage closed")

