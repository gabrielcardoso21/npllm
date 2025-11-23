"""
Modelo LLM via API (Groq, Google Gemini, etc.)
Permite usar modelos prontos sem servir localmente
"""

import os
import time
from typing import Optional, Dict, Any, Generator
import requests
from src.models.interfaces import LLMModelInterface
from src.utils.config import get_config
from src.utils.logging import get_logger
import torch


class APIModel(LLMModelInterface):
    """
    Wrapper para modelos LLM via API
    Suporta Groq e Google Gemini
    """
    
    def __init__(self, provider: str = "groq", api_key: Optional[str] = None):
        """
        Inicializa modelo via API
        
        Args:
            provider: "groq" ou "gemini"
            api_key: Chave da API (ou usa variável de ambiente)
        """
        self.logger = get_logger(self.__class__.__name__)
        self.config = get_config()
        self.provider = provider.lower()
        
        # Obtém API key
        if api_key:
            self.api_key = api_key
        elif self.provider == "groq":
            self.api_key = os.getenv("GROQ_API_KEY")
        elif self.provider == "gemini":
            self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        else:
            raise ValueError(f"Provider desconhecido: {provider}")
        
        if not self.api_key:
            raise ValueError(f"API key não encontrada para {provider}. Defina {provider.upper()}_API_KEY")
        
        # Configurações específicas do provider
        if self.provider == "groq":
            self.base_url = "https://api.groq.com/openai/v1/chat/completions"
            # Modelos disponíveis: llama-3.1-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768
            self.model_name = "llama-3.1-8b-instant"  # Modelo rápido e eficiente
        elif self.provider == "gemini":
            self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
            self.model_name = "gemini-2.0-flash-exp"
        
        # Cache para respostas frequentes
        self.response_cache: Dict[str, str] = {}
        self.cache_size = 500
        
        # Hidden size aproximado (para compatibilidade)
        self._hidden_size = 4096  # Valor padrão
        
        self.logger.info(f"Initializing API model: {self.provider} ({self.model_name})")
    
    def generate(
        self,
        prompt: str,
        max_length: int = 8192,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False,
        **kwargs
    ) -> str:
        """
        Gera texto via API
        
        Args:
            prompt: Texto de entrada
            max_length: Comprimento máximo (aproximado)
            temperature: Temperatura
            top_p: Nucleus sampling
            stream: Se True, retorna generator. Se False, retorna string.
            **kwargs: Argumentos adicionais
        
        Returns:
            Texto gerado (string) ou generator (se stream=True)
        """
        if stream:
            return self._generate_stream(prompt, max_length, temperature, top_p, **kwargs)
        else:
            return self._generate_normal(prompt, max_length, temperature, top_p, **kwargs)
    
    def _generate_normal(
        self,
        prompt: str,
        max_length: int = 8192,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ) -> str:
        """Gera texto completo via API"""
        import time
        start_time = time.time()
        
        # Verifica cache
        cache_key = f"{prompt}_{max_length}_{temperature}_{top_p}"
        if cache_key in self.response_cache:
            self.logger.debug("Cache hit for prompt")
            return self.response_cache[cache_key]
        
        try:
            if self.provider == "groq":
                response = self._call_groq(prompt, max_length, temperature, top_p)
            elif self.provider == "gemini":
                response = self._call_gemini(prompt, max_length, temperature, top_p)
            else:
                raise ValueError(f"Provider não suportado: {self.provider}")
            
            # Adiciona ao cache
            self._update_cache(cache_key, response)
            
            elapsed = time.time() - start_time
            self.logger.info(f"API generation completed in {elapsed:.2f}s, length: {len(response)}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error calling API: {e}")
            raise
    
    def _generate_stream(
        self,
        prompt: str,
        max_length: int = 8192,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ) -> Generator[str, None, None]:
        """Gera texto com streaming via API"""
        try:
            if self.provider == "groq":
                for token in self._call_groq_stream(prompt, max_length, temperature, top_p):
                    yield token
            elif self.provider == "gemini":
                for token in self._call_gemini_stream(prompt, max_length, temperature, top_p):
                    yield token
            else:
                raise ValueError(f"Provider não suportado: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error in API streaming: {e}")
            # Fallback: gera sem streaming
            response = self._generate_normal(prompt, max_length, temperature, top_p, **kwargs)
            yield response
    
    def _call_groq(self, prompt: str, max_length: int, temperature: float, top_p: float) -> str:
        """Chama API do Groq"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": min(max_length, 8192),  # Groq limita a 8192
            "stream": False
        }
        
        response = requests.post(self.base_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def _call_groq_stream(self, prompt: str, max_length: int, temperature: float, top_p: float) -> Generator[str, None, None]:
        """Chama API do Groq com streaming"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": min(max_length, 8192),
            "stream": True
        }
        
        response = requests.post(self.base_url, json=payload, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: '
                    if data_str.strip() == '[DONE]':
                        break
                    try:
                        import json
                        data = json.loads(data_str)
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        continue
    
    def _call_gemini(self, prompt: str, max_length: int, temperature: float, top_p: float) -> str:
        """Chama API do Google Gemini"""
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "topP": top_p,
                "maxOutputTokens": min(max_length, 8192),
            }
        }
        
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    
    def _call_gemini_stream(self, prompt: str, max_length: int, temperature: float, top_p: float) -> Generator[str, None, None]:
        """Chama API do Google Gemini com streaming"""
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "topP": top_p,
                "maxOutputTokens": min(max_length, 8192),
            }
        }
        
        # Gemini streaming usa Server-Sent Events
        response = requests.post(url, json=payload, stream=True, timeout=60)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    try:
                        import json
                        data = json.loads(data_str)
                        if "candidates" in data and len(data["candidates"]) > 0:
                            content = data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        continue
    
    def encode(self, text: str) -> torch.Tensor:
        """
        Gera representação interna do texto
        Para API models, usa embedding simples (placeholder)
        """
        # Para API models, não temos acesso direto aos embeddings
        # Retorna tensor vazio (pode ser melhorado com API de embeddings)
        self.logger.warning("encode() not fully supported for API models")
        return torch.zeros(1, self._hidden_size)
    
    def get_hidden_size(self) -> int:
        """Retorna tamanho da representação interna"""
        return self._hidden_size
    
    def _update_cache(self, key: str, value: str):
        """Atualiza cache, removendo entradas antigas se necessário"""
        if len(self.response_cache) >= self.cache_size:
            oldest_key = next(iter(self.response_cache))
            del self.response_cache[oldest_key]
        
        self.response_cache[key] = value
    
    def clear_cache(self):
        """Limpa cache de respostas"""
        self.response_cache.clear()
    
    def unload_model(self):
        """Descarrega modelo (compatibilidade - API models não precisam)"""
        # API models não carregam modelo localmente, apenas limpa cache
        self.clear_cache()

