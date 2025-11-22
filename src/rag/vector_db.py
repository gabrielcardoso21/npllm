"""
PostgreSQL + pgvector integration
Otimizado para baixa memória
"""

import psycopg2
from psycopg2.extras import execute_values
from psycopg2.pool import ThreadedConnectionPool
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from pgvector.psycopg2 import register_vector

from src.utils.config import get_config
from src.utils.logging import get_logger


class VectorDatabase:
    """
    Interface para PostgreSQL + pgvector
    Otimizado para baixo uso de memória
    """
    
    def __init__(self):
        """Inicializa conexão com PostgreSQL + pgvector"""
        self.logger = get_logger(self.__class__.__name__)
        self.config = get_config()
        db_config = self.config.database
        
        # Configuração de conexão
        self.connection_params = {
            "host": db_config.host,
            "port": db_config.port,
            "database": db_config.database,
            "user": db_config.user,
            "password": db_config.password
        }
        
        # Connection pool (otimizado para baixa memória)
        self.pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=db_config.pool_size,
            **self.connection_params
        )
        
        # Registra extensão pgvector
        conn = self.pool.getconn()
        try:
            register_vector(conn)
            self._initialize_schema(conn)
        finally:
            self.pool.putconn(conn)
        
        self.logger.info("Vector database initialized")
    
    def _initialize_schema(self, conn):
        """Inicializa schema do banco de dados"""
        cursor = conn.cursor()
        
        # Cria tabela de embeddings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_embeddings (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(384),  -- Dimensão padrão para all-MiniLM-L6-v2
                metadata JSONB,
                project_id VARCHAR(255),
                file_path VARCHAR(500),
                function_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cria índice HNSW para busca rápida (otimizado para baixa memória)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS code_embeddings_hnsw_idx 
            ON code_embeddings 
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """)
        
        # Índices adicionais para filtros
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS code_embeddings_project_idx 
            ON code_embeddings (project_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS code_embeddings_metadata_idx 
            ON code_embeddings USING GIN (metadata)
        """)
        
        conn.commit()
        cursor.close()
        self.logger.info("Database schema initialized")
    
    def insert_embeddings(
        self,
        contents: List[str],
        embeddings: np.ndarray,
        metadata: List[Dict[str, Any]],
        project_id: Optional[str] = None
    ):
        """
        Insere embeddings no banco
        
        Args:
            contents: Lista de conteúdos (código)
            embeddings: Array numpy de embeddings [num_items, embedding_dim]
            metadata: Lista de metadados
            project_id: ID do projeto (opcional)
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            
            # Prepara dados para inserção
            data = []
            for i, (content, embedding, meta) in enumerate(zip(contents, embeddings, metadata)):
                data.append((
                    content,
                    embedding.tolist(),  # Converte para lista para pgvector
                    meta,
                    project_id,
                    meta.get("file_path"),
                    meta.get("function_name")
                ))
            
            # Insere em batch
            execute_values(
                cursor,
                """
                INSERT INTO code_embeddings 
                (content, embedding, metadata, project_id, file_path, function_name)
                VALUES %s
                """,
                data
            )
            
            conn.commit()
            cursor.close()
            self.logger.info(f"Inserted {len(contents)} embeddings")
        finally:
            self.pool.putconn(conn)
    
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        project_id: Optional[str] = None,
        similarity_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca similaridade vetorial
        
        Args:
            query_embedding: Embedding da query [embedding_dim]
            top_k: Número de resultados
            project_id: Filtrar por projeto
            similarity_threshold: Threshold de similaridade mínima
            filters: Filtros adicionais em metadata
        
        Returns:
            Lista de resultados com conteúdo e metadados
        """
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            
            # Constrói query
            query = """
                SELECT 
                    id,
                    content,
                    metadata,
                    file_path,
                    function_name,
                    1 - (embedding <=> %s::vector) as similarity
                FROM code_embeddings
                WHERE 1 - (embedding <=> %s::vector) >= %s
            """
            params = [query_embedding.tolist(), query_embedding.tolist(), similarity_threshold]
            
            # Adiciona filtros
            if project_id:
                query += " AND project_id = %s"
                params.append(project_id)
            
            if filters:
                for key, value in filters.items():
                    query += f" AND metadata->>'{key}' = %s"
                    params.append(str(value))
            
            query += " ORDER BY similarity DESC LIMIT %s"
            params.append(top_k)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Formata resultados
            formatted_results = []
            for row in results:
                formatted_results.append({
                    "id": row[0],
                    "content": row[1],
                    "metadata": row[2],
                    "file_path": row[3],
                    "function_name": row[4],
                    "similarity": float(row[5])
                })
            
            cursor.close()
            return formatted_results
        finally:
            self.pool.putconn(conn)
    
    def close(self):
        """Fecha pool de conexões"""
        if self.pool:
            self.pool.closeall()
            self.logger.info("Database connection pool closed")

