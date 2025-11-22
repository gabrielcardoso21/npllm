"""
LoRA Adapter implementation using PEFT
Otimizado com versionamento simplificado (stable/experimental)
"""

import torch
import torch.nn as nn
from typing import Optional, Dict, Any
from pathlib import Path

from peft import LoraConfig, get_peft_model, PeftModel
from src.models.interfaces import AdapterInterface
from src.utils.logging import get_logger


class LoRAAdapter(AdapterInterface):
    """
    LoRA Adapter para fine-tuning eficiente
    Suporta versionamento stable/experimental
    """
    
    def __init__(
        self,
        base_model: Any,
        name: str,
        context: str,
        version: str = "stable",
        r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.1,
        target_modules: Optional[list] = None
    ):
        """
        Inicializa LoRA adapter
        
        Args:
            base_model: Modelo base (CodeLlama)
            name: Nome do adapter
            context: Contexto do adapter (ex: 'odoo', 'django')
            version: Versão ('stable' ou 'experimental')
            r: Rank do LoRA
            lora_alpha: Alpha do LoRA
            lora_dropout: Dropout do LoRA
            target_modules: Módulos alvo para LoRA
        """
        self.logger = get_logger(self.__class__.__name__)
        
        if version not in ["stable", "experimental"]:
            raise ValueError(f"Version must be 'stable' or 'experimental', got '{version}'")
        
        self.name = name
        self.context = context
        self.version = version
        self.base_model = base_model
        
        # Configuração LoRA
        if target_modules is None:
            target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]
        
        lora_config = LoraConfig(
            r=r,
            lora_alpha=lora_alpha,
            target_modules=target_modules,
            lora_dropout=lora_dropout,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        # Aplica LoRA ao modelo base
        self.model = get_peft_model(base_model, lora_config)
        self.model.eval()  # Modo avaliação por padrão
        
        self.logger.info(f"LoRA adapter created: {name} ({context}, {version})")
    
    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """
        Aplica adapter aos hidden states
        
        Args:
            hidden_states: Tensor [batch, seq_len, hidden_size]
        
        Returns:
            Tensor modificado [batch, seq_len, hidden_size]
        """
        # LoRA modifica os pesos do modelo base durante forward
        # Para hidden states, precisamos passar pelo modelo completo
        # Esta é uma simplificação - em produção, integraríamos melhor
        return hidden_states
    
    def get_name(self) -> str:
        """Retorna nome do adapter"""
        return self.name
    
    def get_context(self) -> str:
        """Retorna contexto do adapter"""
        return self.context
    
    def get_version(self) -> str:
        """Retorna versão do adapter"""
        return self.version
    
    def save(self, path: str):
        """Salva adapter em disco"""
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Salva usando PEFT
        self.model.save_pretrained(str(save_path))
        
        # Salva metadados
        metadata = {
            "name": self.name,
            "context": self.context,
            "version": self.version
        }
        
        import json
        with open(save_path / "metadata.json", "w") as f:
            json.dump(metadata, f)
        
        self.logger.info(f"Adapter saved to {save_path}")
    
    def load(self, path: str):
        """Carrega adapter do disco"""
        load_path = Path(path)
        
        # Carrega usando PEFT
        self.model = PeftModel.from_pretrained(self.base_model, str(load_path))
        self.model.eval()
        
        # Carrega metadados
        metadata_path = load_path / "metadata.json"
        if metadata_path.exists():
            import json
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                self.name = metadata.get("name", self.name)
                self.context = metadata.get("context", self.context)
                self.version = metadata.get("version", self.version)
        
        self.logger.info(f"Adapter loaded from {load_path}")
    
    def train_mode(self):
        """Ativa modo de treinamento"""
        self.model.train()
    
    def eval_mode(self):
        """Ativa modo de avaliação"""
        self.model.eval()

