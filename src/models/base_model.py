"""
Modelo base LLM: CodeLlama 3B quantizado 4-bit (GGML)
Wrapper otimizado para CPU com cache e gerenciamento de memória
"""

import torch
from typing import Optional, Dict, Any, List
from pathlib import Path
import gc
from functools import lru_cache

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from src.models.interfaces import LLMModelInterface
from src.utils.config import get_config
from src.utils.logging import get_logger


class CodeLlamaBaseModel(LLMModelInterface):
    """
    Wrapper para CodeLlama 3B quantizado 4-bit
    Otimizado para CPU com cache e lazy loading
    """
    
    def __init__(self, model_path: Optional[str] = None, cache_dir: Optional[str] = None):
        """
        Inicializa modelo base
        
        Args:
            model_path: Caminho para modelo local (opcional)
            cache_dir: Diretório de cache para modelos
        """
        self.logger = get_logger(self.__class__.__name__)
        self.config = get_config()
        model_config = self.config.model
        
        self.model_path = model_path or model_config.base_model
        self.cache_dir = cache_dir or Path("./models/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.device = model_config.device
        self.max_memory = model_config.max_memory
        
        # Cache para respostas frequentes
        self.response_cache: Dict[str, str] = {}
        self.cache_size = 500
        
        # Modelo e tokenizer (lazy loading)
        self._model: Optional[Any] = None
        self._tokenizer: Optional[Any] = None
        self._hidden_size: Optional[int] = None
        
        self.logger.info(f"Initializing CodeLlama base model: {self.model_path}")
    
    def load_model(self):
        """Carrega modelo com quantização 4-bit (método público)"""
        self._load_model()
    
    def _load_model(self):
        """Carrega modelo com quantização 4-bit (lazy loading)"""
        if self._model is not None:
            return
        
        self.logger.info("Loading model with 4-bit quantization...")
        
        # Configuração de quantização 4-bit
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        try:
            # Obtém token do ambiente, cache ou configuração
            import os
            from huggingface_hub import HfFolder
            
            # Tenta múltiplas fontes de token
            hf_token = (
                os.getenv("HF_TOKEN") or 
                os.getenv("HUGGING_FACE_HUB_TOKEN") or
                HfFolder.get_token() or
                None
            )
            
            if not hf_token:
                self.logger.warning("Nenhum token HF encontrado. Modelo pode falhar se for gated.")
            
            # Carrega modelo quantizado
            # Para modelos muito pequenos (TinyLlama), pode não precisar de quantização
            use_quantization = "TinyLlama" not in self.model_path and "phi-2" not in self.model_path
            
            if use_quantization:
                self._model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    quantization_config=quantization_config,
                    device_map="auto",
                    cache_dir=str(self.cache_dir),
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True,
                    token=hf_token,
                    trust_remote_code=True
                )
            else:
                # Modelos pequenos: sem quantização para mais velocidade
                self.logger.info("Loading small model without quantization for faster inference")
                # Usa bfloat16 se disponível (mais rápido que float32), senão float16
                try:
                    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float16
                except:
                    dtype = torch.float16
                self._model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    device_map="auto",
                    cache_dir=str(self.cache_dir),
                    torch_dtype=dtype,  # bfloat16/float16 para mais velocidade
                    low_cpu_mem_usage=True,
                    token=hf_token,
                    trust_remote_code=True
                )
            
            # Carrega tokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                cache_dir=str(self.cache_dir),
                token=hf_token,
                trust_remote_code=True
            )
            
            # Configura padding token se não existir
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token
            
            # Obtém hidden size
            self._hidden_size = self._model.config.hidden_size
            
            self.logger.info(f"Model loaded successfully. Hidden size: {self._hidden_size}")
            
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            raise
    
    def generate(
        self,
        prompt: str,
        max_length: int = 8192,  # Aumentado para 8192 tokens (modelo local, sem custo)
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False,
        **kwargs
    ):
        """
        Gera texto a partir de prompt com cache
        
        Args:
            prompt: Texto de entrada
            max_length: Comprimento máximo
            temperature: Temperatura
            top_p: Nucleus sampling
            stream: Se True, retorna generator. Se False, retorna string.
            **kwargs: Argumentos adicionais
        
        Returns:
            Texto gerado (string) ou generator (se stream=True)
        """
        self.logger.debug(f"generate() called with stream={stream}, prompt_length={len(prompt)}")
        if stream:
            self.logger.debug("Calling _generate_stream()")
            return self._generate_stream(prompt, max_length, temperature, top_p, **kwargs)
        else:
            self.logger.debug("Calling _generate_normal()")
            result = self._generate_normal(prompt, max_length, temperature, top_p, **kwargs)
            self.logger.debug(f"_generate_normal() returned type: {type(result)}, length: {len(result) if isinstance(result, str) else 'N/A'}")
            return result
    
    def _generate_normal(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ) -> str:
        """
        Gera texto completo (não-streaming)
        
        Returns:
            String com texto gerado
        """
        import time
        start_time = time.time()
        self.logger.debug(f"_generate_normal() called with max_length={max_length}")
        
        # Carrega modelo se necessário
        load_start = time.time()
        self._load_model()
        load_time = time.time() - load_start
        if load_time > 0.1:
            self.logger.info(f"Model load time: {load_time:.2f}s")
        
        # Formata prompt para TinyLlama se necessário
        if "TinyLlama" in self.model_path:
            # TinyLlama usa formato de chat simples
            formatted_prompt = f"<|user|>\n{prompt}<|assistant|>\n"
        else:
            formatted_prompt = prompt
        
        # Tokeniza prompt
        tokenize_start = time.time()
        inputs = self._tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
        tokenize_time = time.time() - tokenize_start
        if tokenize_time > 0.1:
            self.logger.debug(f"Tokenization time: {tokenize_time:.2f}s")
        
        # Verifica cache primeiro
        cache_key = f"{prompt}_{max_length}_{temperature}_{top_p}"
        if cache_key in self.response_cache:
            self.logger.debug("Cache hit for prompt")
            return self.response_cache[cache_key]
        
        # Usa max_length fornecido (sem limitação artificial)
        # O usuário controla o tamanho através do parâmetro max_length
        effective_max_length = max_length
        
        # Gera resposta
        gen_start = time.time()
        input_length = inputs.input_ids.shape[1]
        max_new_tokens = max(1, effective_max_length - input_length)  # Garante pelo menos 1 token
        
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,  # Usa max_new_tokens para ser mais preciso
                temperature=temperature,
                top_p=top_p,
                do_sample=temperature > 0,  # Se temperature=0, não faz sampling
                pad_token_id=self._tokenizer.pad_token_id,
                **kwargs
            )
        gen_time = time.time() - gen_start
        self.logger.info(f"Generation time: {gen_time:.2f}s, tokens: {outputs.shape[1] - inputs.input_ids.shape[1]}")
        
        # Decodifica resposta
        decode_start = time.time()
        generated_text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        decode_time = time.time() - decode_start
        
        # Remove prompt da resposta
        # IMPORTANTE: Verificar se o prompt está no início antes de remover
        if generated_text.startswith(formatted_prompt):
            response = generated_text[len(formatted_prompt):].strip()
        elif generated_text.startswith(prompt):
            response = generated_text[len(prompt):].strip()
        else:
            # Se o prompt não estiver no início, pode ser que o modelo tenha reformatado
            # Nesse caso, tenta remover apenas a parte do prompt original
            # Para TinyLlama, remove o formato de chat
            if "<|assistant|>" in generated_text:
                response = generated_text.split("<|assistant|>", 1)[-1].strip()
            else:
                response = generated_text.strip()
        
        # Log para debug
        total_time = time.time() - start_time
        self.logger.info(f"Total generation time: {total_time:.2f}s (load: {load_time:.2f}s, gen: {gen_time:.2f}s, decode: {decode_time:.2f}s)")
        self.logger.debug(f"Generated text length: {len(generated_text)}, Response length: {len(response)}")
        
        # Adiciona ao cache
        self._update_cache(cache_key, response)
        
        self.logger.debug(f"_generate_normal() returning string of length {len(response)}")
        return response
    
    def _generate_stream(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ):
        """
        Gera texto com streaming (generator)
        
        Yields:
            Tokens conforme são gerados
        """
        import time
        start_time = time.time()
        
        # Carrega modelo se necessário
        self._load_model()
        
        # Formata prompt para TinyLlama se necessário (igual ao _generate_normal)
        if "TinyLlama" in self.model_path:
            formatted_prompt = f"<|user|>\n{prompt}<|assistant|>\n"
        else:
            formatted_prompt = prompt
        
        # Tokeniza prompt
        inputs = self._tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
        
        # Usa max_length fornecido (sem limitação artificial)
        input_length = inputs.input_ids.shape[1]
        max_new_tokens = max(1, max_length - input_length)
        
        # Modo streaming: retorna generator
        from transformers import TextIteratorStreamer
        from threading import Thread
        import queue
        
        streamer = TextIteratorStreamer(
            self._tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
            timeout=60.0  # Timeout para evitar travamento
        )
        
        # Inicia geração em thread separada
        generation_kwargs = {
            **inputs,
            "max_new_tokens": max_new_tokens,  # Usa max_new_tokens como no _generate_normal
            "temperature": temperature,
            "top_p": top_p,
            "do_sample": temperature > 0,
            "pad_token_id": self._tokenizer.pad_token_id,
            "streamer": streamer,
            **kwargs
        }
        
        thread = Thread(target=self._model.generate, kwargs=generation_kwargs, daemon=True)
        thread.start()
        
        # Yield tokens conforme são gerados
        try:
            for token in streamer:
                if token:
                    yield token
            # Aguarda thread terminar para evitar erro de cleanup
            thread.join(timeout=1.0)
        except Exception as e:
            self.logger.error(f"Error in streaming: {e}")
            # Aguarda thread terminar antes do fallback
            thread.join(timeout=1.0)
            # Fallback: gera sem streaming
            self.logger.warning("Falling back to non-streaming generation")
            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=temperature > 0,
                    pad_token_id=self._tokenizer.pad_token_id,
                    **kwargs
                )
            generated_text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            if generated_text.startswith(formatted_prompt):
                response = generated_text[len(formatted_prompt):].strip()
            else:
                response = generated_text.strip()
            # Yield resposta completa como fallback
            yield response
        finally:
            # Garante que a thread termine corretamente
            if thread.is_alive():
                thread.join(timeout=0.5)
    
    def encode(self, text: str) -> torch.Tensor:
        """
        Gera representação interna do texto
        
        Args:
            text: Texto de entrada
        
        Returns:
            Tensor [seq_len, hidden_size]
        """
        self._load_model()
        
        inputs = self._tokenizer(text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self._model(**inputs, output_hidden_states=True)
            # Retorna hidden states da última camada
            hidden_states = outputs.hidden_states[-1]
        
        return hidden_states[0]  # Remove batch dimension
    
    def get_hidden_size(self) -> int:
        """Retorna tamanho da representação interna"""
        if self._hidden_size is None:
            self._load_model()
        return self._hidden_size
    
    def _update_cache(self, key: str, value: str):
        """Atualiza cache, removendo entradas antigas se necessário"""
        if len(self.response_cache) >= self.cache_size:
            # Remove entrada mais antiga (FIFO simples)
            oldest_key = next(iter(self.response_cache))
            del self.response_cache[oldest_key]
        
        self.response_cache[key] = value
    
    def clear_cache(self):
        """Limpa cache de respostas"""
        self.response_cache.clear()
        gc.collect()
    
    def unload_model(self):
        """Descarrega modelo da memória"""
        if self._model is not None:
            del self._model
            del self._tokenizer
            self._model = None
            self._tokenizer = None
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            self.logger.info("Model unloaded from memory")

