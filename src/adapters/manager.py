"""
Adapter Manager
Gerencia carregamento e aplicação de adapters LoRA
"""

from typing import Optional, Dict, Any
from pathlib import Path
import torch
from peft import PeftModel

from src.adapters.lora_adapter import LoRAAdapter
from src.adapters.versioning import AdapterVersioning
from src.utils.logging import get_logger


class AdapterManager:
    """
    Gerencia adapters LoRA
    Carrega, versiona e aplica adapters ao modelo base
    """
    
    def __init__(self, base_model):
        """
        Inicializa gerenciador de adapters
        
        Args:
            base_model: Modelo base (CodeLlamaBaseModel)
        """
        self.logger = get_logger(self.__class__.__name__)
        self.base_model = base_model
        self.versioning = AdapterVersioning()
        self.adapters_dir = Path("./adapters")
        self.adapters_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache de adapters carregados (objetos LoRAAdapter)
        self._loaded_adapters: Dict[str, Any] = {}
        # Cache de adapters carregados no modelo (PeftModel)
        self._loaded_models: Dict[str, Any] = {}
        self._current_adapter: Optional[str] = None
        
        self.logger.info("Adapter manager initialized")
    
    def get_adapter(self, adapter_name: str, prefer_stable: bool = True) -> Optional[LoRAAdapter]:
        """
        Obtém adapter por nome
        
        Args:
            adapter_name: Nome do adapter
            prefer_stable: Se True, prefere versão stable
        
        Returns:
            Adapter ou None se não encontrado
        """
        # Verifica se adapter existe
        adapter_path = self.adapters_dir / adapter_name
        
        if not adapter_path.exists():
            self.logger.debug(f"Adapter {adapter_name} not found")
            return None
        
        # Obtém versão preferida
        version = self.versioning.get_preferred_version(adapter_name, prefer_stable)
        version_path = adapter_path / version
        
        if not version_path.exists():
            self.logger.warning(f"Adapter {adapter_name} version {version} not found")
            return None
        
        # Carrega adapter
        try:
            adapter = LoRAAdapter.load(str(version_path))
            return adapter
        except Exception as e:
            self.logger.error(f"Error loading adapter {adapter_name}: {e}")
            return None
    
    def load_adapter_for_generation(self, adapter_name: str, base_model_instance) -> bool:
        """
        Carrega adapter no modelo base para geração
        
        IMPORTANTE: LoRA adapters são aplicados via PEFT durante a geração do modelo
        Este método carrega o adapter no modelo base usando PeftModel
        
        Args:
            adapter_name: Nome do adapter
            base_model_instance: Instância do modelo base
        
        Returns:
            True se carregado com sucesso
        """
        # Se já está carregado, não precisa recarregar
        if self._current_adapter == adapter_name and adapter_name in self._loaded_models:
            return True
        
        try:
            # Obtém adapter
            adapter = self.get_adapter(adapter_name, prefer_stable=True)
            if not adapter:
                return False
            
            # Carrega modelo se necessário
            if base_model_instance._model is None:
                base_model_instance._load_model()
            
            model = base_model_instance._model
            adapter_path = self.adapters_dir / adapter_name / "stable"
            
            if not adapter_path.exists():
                adapter_path = self.adapters_dir / adapter_name / "experimental"
            
            if adapter_path.exists():
                # Carrega adapter usando PEFT
                # IMPORTANTE: PeftModel.from_pretrained modifica o modelo base
                # Os pesos do adapter são aplicados durante a geração
                model = PeftModel.from_pretrained(model, str(adapter_path))
                base_model_instance._model = model
                
                self._loaded_models[adapter_name] = model
                self._current_adapter = adapter_name
                
                self.logger.info(f"Adapter {adapter_name} loaded for generation")
                return True
            else:
                self.logger.warning(f"Adapter path not found: {adapter_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading adapter {adapter_name} for generation: {e}")
            return False
    
    def unload_adapter(self):
        """Descarrega adapter atual do modelo"""
        if self._current_adapter:
            # PEFT não tem método direto para descarregar
            # Recarrega modelo base sem adapter
            if self.base_model._model:
                # Salva referência ao modelo base original
                # Por enquanto, apenas limpa cache
                self._current_adapter = None
                self.logger.info("Adapter unloaded")
    
    def list_adapters(self) -> list:
        """Lista todos os adapters disponíveis"""
        adapters = []
        for adapter_dir in self.adapters_dir.iterdir():
            if adapter_dir.is_dir():
                adapters.append({
                    "name": adapter_dir.name,
                    "versions": list(adapter_dir.iterdir())
                })
        return adapters
