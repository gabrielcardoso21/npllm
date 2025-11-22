"""
Gerenciador de adapters LoRA
Lazy loading e gerenciamento de múltiplos adapters simultâneos
"""

from typing import Dict, Optional, List
from pathlib import Path

from src.adapters.lora_adapter import LoRAAdapter
from src.adapters.versioning import AdapterVersionManager, AdapterVersion
from src.models.base_model import CodeLlamaBaseModel
from src.utils.config import get_config
from src.utils.logging import get_logger


class AdapterManager:
    """
    Gerenciador de adapters com lazy loading
    Otimizado para reduzir uso de memória
    """
    
    def __init__(self, base_model: CodeLlamaBaseModel):
        """
        Inicializa gerenciador de adapters
        
        Args:
            base_model: Modelo base CodeLlama
        """
        self.logger = get_logger(self.__class__.__name__)
        self.base_model = base_model
        self.config = get_config()
        
        # Version manager
        self.version_manager = AdapterVersionManager()
        
        # Adapters carregados em memória (lazy loading)
        self._loaded_adapters: Dict[str, LoRAAdapter] = {}
        # Chave: "{context}_{version}"
        
        # Configuração de adapters
        adapter_config = self.config.get_section("adapters")
        lora_config = adapter_config.get("lora", {})
        
        self.lora_r = lora_config.get("r", 16)
        self.lora_alpha = lora_config.get("lora_alpha", 32)
        self.lora_dropout = lora_config.get("lora_dropout", 0.1)
        self.target_modules = lora_config.get("target_modules", ["q_proj", "v_proj", "k_proj", "o_proj"])
    
    def create_adapter(
        self,
        name: str,
        context: str,
        version: str = "stable"
    ) -> LoRAAdapter:
        """
        Cria novo adapter
        
        Args:
            name: Nome do adapter
            context: Contexto (ex: 'odoo', 'django')
            version: Versão ('stable' ou 'experimental')
        
        Returns:
            Adapter criado
        """
        adapter = LoRAAdapter(
            base_model=self.base_model._model if self.base_model._model else self.base_model,
            name=name,
            context=context,
            version=version,
            r=self.lora_r,
            lora_alpha=self.lora_alpha,
            lora_dropout=self.lora_dropout,
            target_modules=self.target_modules
        )
        
        self.version_manager.register(adapter, context, version)
        
        return adapter
    
    def load_adapter(
        self,
        context: str,
        version: Optional[str] = None,
        prefer_stable: bool = True
    ) -> Optional[LoRAAdapter]:
        """
        Carrega adapter (lazy loading)
        
        Args:
            context: Contexto do adapter
            version: Versão específica (None para automático)
            prefer_stable: Se True, prefere stable quando version=None
        
        Returns:
            Adapter carregado ou None
        """
        # Verifica se já está carregado
        cache_key = f"{context}_{version or 'auto'}"
        if cache_key in self._loaded_adapters:
            self.logger.debug(f"Adapter already loaded: {cache_key}")
            return self._loaded_adapters[cache_key]
        
        # Tenta obter do version manager
        adapter = self.version_manager.get(context, version, prefer_stable)
        
        if adapter is None:
            self.logger.warning(f"Adapter not found: {context}/{version}")
            return None
        
        # Carrega em memória
        self._loaded_adapters[cache_key] = adapter
        self.logger.info(f"Adapter loaded: {cache_key}")
        
        return adapter
    
    def unload_adapter(self, context: str, version: Optional[str] = None):
        """
        Descarrega adapter da memória
        
        Args:
            context: Contexto do adapter
            version: Versão específica
        """
        cache_key = f"{context}_{version or 'auto'}"
        if cache_key in self._loaded_adapters:
            del self._loaded_adapters[cache_key]
            self.logger.info(f"Adapter unloaded: {cache_key}")
    
    def get_adapter(
        self,
        context: str,
        version: Optional[str] = None,
        prefer_stable: bool = True
    ) -> Optional[LoRAAdapter]:
        """
        Obtém adapter (carrega se necessário)
        
        Args:
            context: Contexto do adapter
            version: Versão específica
            prefer_stable: Preferir stable
        
        Returns:
            Adapter ou None
        """
        return self.load_adapter(context, version, prefer_stable)
    
    def list_adapters(self, context: Optional[str] = None) -> List[Dict[str, str]]:
        """Lista adapters disponíveis"""
        return self.version_manager.list_adapters(context)
    
    def save_adapter(self, adapter: LoRAAdapter, path: Optional[str] = None):
        """Salva adapter em disco"""
        if path is None:
            path = f"./adapters/{adapter.get_context()}/{adapter.get_version()}"
        
        adapter.save(path)
    
    def promote_to_stable(self, context: str) -> bool:
        """Promove adapter experimental para stable"""
        return self.version_manager.promote_to_stable(context)

