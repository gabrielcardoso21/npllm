"""
Interfaces plugáveis para modelos LLM, embeddings e adapters
Permite trocar implementações facilmente
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import torch


class EmbeddingModelInterface(ABC):
    """Interface para modelos de embedding (plugável)"""
    
    @abstractmethod
    def encode(self, texts: List[str], batch_size: int = 32) -> torch.Tensor:
        """
        Gera embeddings para textos
        
        Args:
            texts: Lista de textos para gerar embeddings
            batch_size: Tamanho do batch para processamento
        
        Returns:
            Tensor com embeddings [num_texts, embedding_dim]
        """
        pass
    
    @abstractmethod
    def get_embedding_dim(self) -> int:
        """Retorna dimensão dos embeddings"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Retorna nome do modelo"""
        pass


class LLMModelInterface(ABC):
    """Interface para modelos LLM (plugável)"""
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ) -> str:
        """
        Gera texto a partir de prompt
        
        Args:
            prompt: Texto de entrada
            max_length: Comprimento máximo da saída
            temperature: Temperatura para sampling
            top_p: Nucleus sampling parameter
            **kwargs: Argumentos adicionais
        
        Returns:
            Texto gerado
        """
        pass
    
    @abstractmethod
    def encode(self, text: str) -> torch.Tensor:
        """
        Gera representação interna do texto
        
        Args:
            text: Texto de entrada
        
        Returns:
            Tensor com representação [seq_len, hidden_size]
        """
        pass
    
    @abstractmethod
    def get_hidden_size(self) -> int:
        """Retorna tamanho da representação interna"""
        pass


class AdapterInterface(ABC):
    """Interface para adapters LoRA (plugável)"""
    
    @abstractmethod
    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """
        Aplica adapter aos hidden states
        
        Args:
            hidden_states: Tensor [batch, seq_len, hidden_size]
        
        Returns:
            Tensor modificado [batch, seq_len, hidden_size]
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna nome do adapter"""
        pass
    
    @abstractmethod
    def get_context(self) -> str:
        """Retorna contexto do adapter (ex: 'odoo', 'django')"""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Retorna versão do adapter (stable ou experimental)"""
        pass
    
    @abstractmethod
    def save(self, path: str):
        """Salva adapter em disco"""
        pass
    
    @abstractmethod
    def load(self, path: str):
        """Carrega adapter do disco"""
        pass

