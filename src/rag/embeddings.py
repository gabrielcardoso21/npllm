"""
Sistema de embeddings plugável
Suporta diferentes providers: Sentence Transformers, CodeBERT, etc.
"""

import torch
import numpy as np
from typing import List, Optional
from abc import ABC, abstractmethod

from sentence_transformers import SentenceTransformer

from src.models.interfaces import EmbeddingModelInterface
from src.utils.config import get_config
from src.utils.logging import get_logger


class SentenceTransformersEmbedding(EmbeddingModelInterface):
    """Implementação usando Sentence Transformers"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        """
        Inicializa Sentence Transformers
        
        Args:
            model_name: Nome do modelo
            device: Dispositivo (cpu ou cuda)
        """
        self.logger = get_logger(self.__class__.__name__)
        self.model_name = model_name
        self.device = device
        
        self.logger.info(f"Loading Sentence Transformers model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        self._embedding_dim = self.model.get_sentence_embedding_dimension()
        
        self.logger.info(f"Model loaded. Embedding dimension: {self._embedding_dim}")
    
    def encode(self, texts: List[str], batch_size: int = 32) -> torch.Tensor:
        """Gera embeddings"""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        return embeddings
    
    def get_embedding_dim(self) -> int:
        """Retorna dimensão dos embeddings"""
        return self._embedding_dim
    
    def get_model_name(self) -> str:
        """Retorna nome do modelo"""
        return self.model_name


class EmbeddingProvider:
    """
    Factory para criar providers de embedding
    Sistema plugável
    """
    
    _providers = {
        "sentence_transformers": SentenceTransformersEmbedding,
        # Adicionar outros providers aqui:
        # "codebert": CodeBERTEmbedding,
        # "openai": OpenAIEmbedding,
    }
    
    @classmethod
    def create(
        cls,
        provider: str = "sentence_transformers",
        model_name: Optional[str] = None,
        device: str = "cpu"
    ) -> EmbeddingModelInterface:
        """
        Cria provider de embedding
        
        Args:
            provider: Nome do provider
            model_name: Nome do modelo (opcional)
            device: Dispositivo
        
        Returns:
            Instância do provider
        """
        if provider not in cls._providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls._providers.keys())}")
        
        provider_class = cls._providers[provider]
        
        # Se não especificar model_name, usa configuração padrão
        if model_name is None:
            config = get_config()
            embeddings_config = config.get_section("embeddings")
            model_name = embeddings_config.get("model", "sentence-transformers/all-MiniLM-L6-v2")
        
        return provider_class(model_name=model_name, device=device)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """
        Registra novo provider
        
        Args:
            name: Nome do provider
            provider_class: Classe do provider (deve implementar EmbeddingModelInterface)
        """
        cls._providers[name] = provider_class

