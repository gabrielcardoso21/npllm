"""
Feedback implícito: comportamento do usuário
Detecta aceita, edita, deleta código
"""

from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

from src.utils.logging import get_logger


class UserAction(Enum):
    """Ações do usuário"""
    ACCEPT = "accept"
    EDIT = "edit"
    DELETE = "delete"
    IGNORE = "ignore"


class ImplicitFeedback:
    """
    Sistema de feedback implícito
    Detecta comportamento do usuário para calcular recompensas
    """
    
    def __init__(self):
        """Inicializa sistema de feedback implícito"""
        self.logger = get_logger(self.__class__.__name__)
        self.interaction_history: list = []
    
    def track_interaction(
        self,
        suggestion_id: str,
        user_action: UserAction,
        edit_distance: Optional[float] = None,
        time_to_action: Optional[float] = None
    ):
        """
        Registra interação do usuário
        
        Args:
            suggestion_id: ID da sugestão
            user_action: Ação do usuário
            edit_distance: Distância de edição (se editou)
            time_to_action: Tempo até ação (em segundos)
        """
        interaction = {
            "suggestion_id": suggestion_id,
            "action": user_action.value,
            "edit_distance": edit_distance,
            "time_to_action": time_to_action,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.interaction_history.append(interaction)
        self.logger.debug(f"Interaction tracked: {suggestion_id} - {user_action.value}")
    
    def calculate_reward(
        self,
        user_action: UserAction,
        edit_distance: Optional[float] = None,
        time_to_action: Optional[float] = None
    ) -> float:
        """
        Calcula recompensa baseada em comportamento
        
        Args:
            user_action: Ação do usuário
            edit_distance: Distância de edição (0.0 = sem edição, 1.0 = muito diferente)
            time_to_action: Tempo até ação
        
        Returns:
            Recompensa (-1.0 a +1.0)
        """
        if user_action == UserAction.ACCEPT:
            # Aceitou sem editar = recompensa máxima
            if edit_distance is None or edit_distance < 0.1:
                return 1.0
            # Aceitou com pequena edição = recompensa alta
            elif edit_distance < 0.3:
                return 0.8
            # Aceitou com edição moderada = recompensa média
            elif edit_distance < 0.6:
                return 0.5
            # Aceitou com muita edição = recompensa baixa
            else:
                return 0.2
        
        elif user_action == UserAction.EDIT:
            # Editou = recompensa parcial (depende da distância)
            if edit_distance is None:
                return 0.3
            elif edit_distance < 0.3:
                return 0.5
            elif edit_distance < 0.6:
                return 0.2
            else:
                return -0.2
        
        elif user_action == UserAction.DELETE:
            # Deletou = recompensa negativa
            return -0.5
        
        elif user_action == UserAction.IGNORE:
            # Ignorou = recompensa negativa leve
            return -0.1
        
        return 0.0
    
    def get_recent_interactions(self, limit: int = 100) -> list:
        """Retorna interações recentes"""
        return self.interaction_history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de interações"""
        if not self.interaction_history:
            return {
                "total": 0,
                "accept_rate": 0.0,
                "edit_rate": 0.0,
                "delete_rate": 0.0,
                "ignore_rate": 0.0
            }
        
        total = len(self.interaction_history)
        actions = [i["action"] for i in self.interaction_history]
        
        return {
            "total": total,
            "accept_rate": actions.count("accept") / total,
            "edit_rate": actions.count("edit") / total,
            "delete_rate": actions.count("delete") / total,
            "ignore_rate": actions.count("ignore") / total,
            "average_reward": sum(
                self.calculate_reward(UserAction(a["action"]), a.get("edit_distance"))
                for a in self.interaction_history
            ) / total
        }

