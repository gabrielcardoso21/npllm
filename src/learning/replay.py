"""
Replay system: Mix old examples with new ones
Prioritizes patterns that generate satisfaction
"""

from typing import List, Dict, Any
from src.utils.logging import get_logger


class ReplaySystem:
    """
    Sistema de replay: Mistura exemplos antigos com novos
    Prioriza padrões que geram satisfação
    """
    
    def __init__(self, replay_ratio: float = 0.3):
        """
        Inicializa sistema de replay
        
        Args:
            replay_ratio: Proporção de exemplos antigos vs. novos (0.0 a 1.0)
        """
        self.logger = get_logger(self.__class__.__name__)
        self.replay_ratio = replay_ratio
        self.logger.info(f"Replay system initialized (ratio: {replay_ratio})")
    
    def mix_examples(
        self,
        old_examples: List[Dict[str, Any]],
        new_examples: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Mistura exemplos antigos com novos
        
        Args:
            old_examples: Exemplos antigos importantes
            new_examples: Novos exemplos (feedback positivo)
        
        Returns:
            Dataset misturado
        """
        if not old_examples:
            self.logger.debug("No old examples, using only new examples")
            return new_examples
        
        if not new_examples:
            self.logger.debug("No new examples, using only old examples")
            return old_examples
        
        # Calcula quantos exemplos antigos usar
        total_examples = len(new_examples)
        num_old = int(total_examples * self.replay_ratio)
        
        # Seleciona exemplos antigos mais importantes (prioriza satisfação)
        old_sorted = sorted(
            old_examples,
            key=lambda x: x.get('score', 0),
            reverse=True
        )
        selected_old = old_sorted[:num_old]
        
        # Mistura: novos primeiro, depois antigos
        mixed = new_examples + selected_old
        
        self.logger.info(
            f"Mixed {len(new_examples)} new examples with {len(selected_old)} old examples"
        )
        
        return mixed
    
    def prioritize_by_satisfaction(
        self,
        examples: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Prioriza exemplos por satisfação (score mais alto primeiro)
        
        Args:
            examples: Lista de exemplos
        
        Returns:
            Exemplos ordenados por satisfação
        """
        return sorted(
            examples,
            key=lambda x: x.get('score', 0),
            reverse=True
        )

