"""
Content Processor
Processes and structures collected content
"""

from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from src.utils.logging import get_logger


class ContentProcessor:
    """
    Processador de conteúdo
    Processa e estrutura conteúdo coletado
    """
    
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Inicializa processador de conteúdo
        
        Args:
            embedding_model: Modelo para geração de embeddings
        """
        self.logger = get_logger(self.__class__.__name__)
        self.embedding_model_name = embedding_model
        self.embedding_model = SentenceTransformer(embedding_model)
        self.logger.info(f"Content processor initialized with model: {embedding_model}")
    
    def process_content(
        self,
        content: str,
        course_id: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Processa conteúdo e retorna chunks processados
        
        Args:
            content: Conteúdo a processar
            course_id: ID do curso
            metadata: Metadados adicionais
        
        Returns:
            Lista de chunks processados
        """
        self.logger.info(f"Processing content for course {course_id}")
        
        # Chunking
        chunks = self.chunk_content(content, chunk_size=512)
        
        # Processa cada chunk
        processed_chunks = []
        for idx, chunk in enumerate(chunks):
            # Extrai metadados
            chunk_metadata = self.extract_metadata(chunk, metadata)
            
            # Gera embedding
            embedding = self.embedding_model.encode(chunk, convert_to_numpy=True)
            
            processed_chunks.append({
                "content": chunk,
                "chunk_index": idx,
                "metadata": chunk_metadata,
                "embedding": embedding
            })
        
        self.logger.info(f"Processed {len(processed_chunks)} chunks")
        return processed_chunks
    
    def chunk_content(
        self,
        content: str,
        chunk_size: int = 512,
        overlap: int = 50
    ) -> List[str]:
        """
        Divide conteúdo em chunks
        
        Args:
            content: Conteúdo a dividir
            chunk_size: Tamanho do chunk (em tokens aproximados)
            overlap: Sobreposição entre chunks
        
        Returns:
            Lista de chunks
        """
        # Aproximação: 1 token ≈ 4 caracteres
        char_size = chunk_size * 4
        char_overlap = overlap * 4
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + char_size
            
            # Tenta quebrar em quebra de linha ou espaço
            if end < len(content):
                # Procura última quebra de linha antes do fim
                last_newline = content.rfind('\n', start, end)
                if last_newline > start:
                    end = last_newline + 1
                else:
                    # Procura último espaço
                    last_space = content.rfind(' ', start, end)
                    if last_space > start:
                        end = last_space + 1
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Próximo chunk com overlap
            start = end - char_overlap
            if start >= len(content):
                break
        
        return chunks
    
    def extract_metadata(
        self,
        content: str,
        base_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extrai metadados do conteúdo
        
        Args:
            content: Conteúdo
            base_metadata: Metadados base
        
        Returns:
            Dicionário com metadados
        """
        metadata = base_metadata.copy() if base_metadata else {}
        
        # Detecta tipo de conteúdo
        if '```' in content:
            metadata['has_code'] = True
        
        # Detecta seções (markdown headers)
        lines = content.split('\n')
        headers = [line.strip() for line in lines if line.strip().startswith('#')]
        if headers:
            metadata['headers'] = headers[:3]  # Primeiros 3 headers
        
        # Tamanho do chunk
        metadata['chunk_length'] = len(content)
        
        return metadata
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Gera embedding para um texto
        
        Args:
            text: Texto
        
        Returns:
            Embedding vetorial
        """
        return self.embedding_model.encode(text, convert_to_numpy=True)

