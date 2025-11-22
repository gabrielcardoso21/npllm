"""
Sistema de retrieval RAG sob demanda
Só busca quando contexto não é suficiente
"""

import numpy as np
from typing import List, Dict, Any, Optional

from src.rag.vector_db import VectorDatabase
from src.rag.embeddings import EmbeddingProvider
from src.utils.config import get_config
from src.utils.logging import get_logger


class RAGRetriever:
    """
    Sistema de retrieval RAG sob demanda (otimizado)
    Só busca quando contexto não é suficiente
    """
    
    def __init__(
        self,
        vector_db: VectorDatabase,
        embedding_provider: Optional[Any] = None
    ):
        """
        Inicializa retriever RAG
        
        Args:
            vector_db: Instância do VectorDatabase
            embedding_provider: Provider de embeddings (opcional, cria se None)
        """
        self.logger = get_logger(self.__class__.__name__)
        self.config = get_config()
        self.vector_db = vector_db
        
        # Configuração RAG
        rag_config = self.config.rag
        self.on_demand = rag_config.on_demand
        self.top_k = rag_config.top_k
        self.similarity_threshold = rag_config.similarity_threshold
        
        # Provider de embeddings
        if embedding_provider is None:
            embeddings_config = self.config.get_section("embeddings")
            provider_name = embeddings_config.get("provider", "sentence_transformers")
            model_name = embeddings_config.get("model", "sentence-transformers/all-MiniLM-L6-v2")
            device = embeddings_config.get("device", "cpu")
            
            self.embedding_provider = EmbeddingProvider.create(
                provider=provider_name,
                model_name=model_name,
                device=device
            )
        else:
            self.embedding_provider = embedding_provider
        
        self.logger.info(f"RAG Retriever initialized (on_demand={self.on_demand})")
    
    def retrieve(
        self,
        query: str,
        project_id: Optional[str] = None,
        force: bool = False,
        filters: Optional[Dict[str, Any]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Busca contexto relevante (sob demanda)
        
        Args:
            query: Query de busca
            project_id: ID do projeto (opcional)
            force: Força busca mesmo se on_demand=False (ignora threshold)
            filters: Filtros adicionais
        
        Returns:
            Lista de resultados ou None se não buscar
        """
        # Se on_demand e não forçar, avalia se precisa buscar
        if self.on_demand and not force:
            # Em produção, aqui avaliaríamos se o contexto atual é suficiente
            # Por enquanto, sempre busca se on_demand está ativo
            # Mas podemos adicionar lógica de avaliação aqui
            pass
        
        # Gera embedding da query
        query_embedding = self.embedding_provider.encode([query])[0]
        query_embedding_np = query_embedding.cpu().numpy()
        
        # Busca no vector database
        results = self.vector_db.search(
            query_embedding=query_embedding_np,
            top_k=self.top_k,
            project_id=project_id,
            similarity_threshold=self.similarity_threshold,
            filters=filters
        )
        
        if not results:
            self.logger.debug("No results found in RAG")
            return None
        
        self.logger.info(f"Retrieved {len(results)} results from RAG")
        return results
    
    def should_use_rag(
        self,
        current_context: Optional[str] = None,
        query: Optional[str] = None
    ) -> bool:
        """
        Decide se deve usar RAG (avaliação de necessidade)
        
        Args:
            current_context: Contexto atual disponível
            query: Query do usuário
        
        Returns:
            True se deve buscar no RAG
        """
        if not self.on_demand:
            return True  # Sempre usa RAG se não for on_demand
        
        # Lógica de avaliação: se contexto atual é vazio ou muito curto, busca
        if not current_context or len(current_context.split()) < 50:
            return True
        
        # Em produção, aqui adicionaríamos mais lógica:
        # - Análise de similaridade entre query e contexto
        # - Análise de confiança do modelo base
        # - etc.
        
        return False  # Por padrão, não busca se tem contexto suficiente
    
    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Formata resultados do RAG como contexto para o modelo
        
        Args:
            results: Resultados da busca
        
        Returns:
            Contexto formatado
        """
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[{i}] File: {result.get('file_path', 'unknown')}\n"
                f"Function: {result.get('function_name', 'unknown')}\n"
                f"Code:\n{result['content']}\n"
            )
        
        return "\n---\n".join(context_parts)

