"""
Sistema de versionamento simplificado: stable + experimental
Otimizado para reduzir memória e complexidade
"""

from typing import Dict, Optional, List
from enum import Enum
from pathlib import Path

from src.adapters.lora_adapter import LoRAAdapter
from src.utils.logging import get_logger


class AdapterVersion(Enum):
    """Versões de adapter suportadas"""
    STABLE = "stable"
    EXPERIMENTAL = "experimental"


class AdapterVersionManager:
    """
    Gerenciador de versionamento de adapters
    Suporta apenas stable e experimental (otimizado)
    """
    
    def __init__(self, adapters_dir: str = "./adapters"):
        """
        Inicializa gerenciador de versionamento
        
        Args:
            adapters_dir: Diretório para armazenar adapters
        """
        self.logger = get_logger(self.__class__.__name__)
        self.adapters_dir = Path(adapters_dir)
        self.adapters_dir.mkdir(parents=True, exist_ok=True)
        
        # Registro de adapters por contexto e versão
        self._adapters: Dict[str, Dict[str, LoRAAdapter]] = {}
        # Estrutura: {context: {version: adapter}}
    
    def get_adapter_path(self, adapter_id: str, version: str = "stable") -> str:
        """
        Retorna caminho para adapter específico
        
        Args:
            adapter_id: ID do adapter
            version: Versão (stable ou experimental)
        
        Returns:
            Caminho do adapter
        """
        return str(self.adapters_dir / adapter_id / version)
    
    def register(
        self,
        adapter: LoRAAdapter,
        context: Optional[str] = None,
        version: Optional[str] = None
    ):
        """
        Registra adapter
        
        Args:
            adapter: Adapter LoRA
            context: Contexto (se None, usa do adapter)
            version: Versão (se None, usa do adapter)
        """
        context = context or adapter.get_context()
        version = version or adapter.get_version()
        
        if version not in [v.value for v in AdapterVersion]:
            raise ValueError(f"Version must be 'stable' or 'experimental', got '{version}'")
        
        if context not in self._adapters:
            self._adapters[context] = {}
        
        self._adapters[context][version] = adapter
        self.logger.info(f"Adapter registered: {context}/{version}")
    
    def get(
        self,
        context: str,
        version: Optional[str] = None,
        prefer_stable: bool = True
    ) -> Optional[LoRAAdapter]:
        """
        Obtém adapter por contexto e versão
        
        Args:
            context: Contexto do adapter
            version: Versão desejada (None para automático)
            prefer_stable: Se True e version=None, prefere stable
        
        Returns:
            Adapter ou None se não encontrado
        """
        if context not in self._adapters:
            self.logger.warning(f"Context not found: {context}")
            return None
        
        context_adapters = self._adapters[context]
        
        if version:
            return context_adapters.get(version)
        
        # Seleção automática
        if prefer_stable and AdapterVersion.STABLE.value in context_adapters:
            return context_adapters[AdapterVersion.STABLE.value]
        elif AdapterVersion.EXPERIMENTAL.value in context_adapters:
            return context_adapters[AdapterVersion.EXPERIMENTAL.value]
        elif AdapterVersion.STABLE.value in context_adapters:
            return context_adapters[AdapterVersion.STABLE.value]
        
        return None
    
    def list_adapters(self, context: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Lista adapters disponíveis
        
        Args:
            context: Filtrar por contexto (None para todos)
        
        Returns:
            Lista de adapters com metadados
        """
        adapters_list = []
        
        contexts = [context] if context else self._adapters.keys()
        
        for ctx in contexts:
            if ctx not in self._adapters:
                continue
            
            for version, adapter in self._adapters[ctx].items():
                adapters_list.append({
                    "name": adapter.get_name(),
                    "context": ctx,
                    "version": version
                })
        
        return adapters_list
    
    def promote_to_stable(self, context: str) -> bool:
        """
        Promove adapter experimental para stable
        
        Args:
            context: Contexto do adapter
        
        Returns:
            True se promovido com sucesso
        """
        if context not in self._adapters:
            return False
        
        context_adapters = self._adapters[context]
        
        if AdapterVersion.EXPERIMENTAL.value not in context_adapters:
            self.logger.warning(f"No experimental adapter found for context: {context}")
            return False
        
        experimental = context_adapters[AdapterVersion.EXPERIMENTAL.value]
        
        # Cria novo adapter stable baseado no experimental
        # Em produção, faríamos backup do stable anterior
        context_adapters[AdapterVersion.STABLE.value] = experimental
        experimental.version = AdapterVersion.STABLE.value
        
        self.logger.info(f"Adapter promoted to stable: {context}")
        return True
    
    def save_all(self, base_path: Optional[str] = None):
        """Salva todos os adapters"""
        base_path = Path(base_path) if base_path else self.adapters_dir
        
        for context, versions in self._adapters.items():
            for version, adapter in versions.items():
                adapter_path = base_path / context / version
                adapter.save(str(adapter_path))

