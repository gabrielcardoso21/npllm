"""
Sleep system: Consolidation during inactivity
Detects inactivity, extracts feedback, filters positive, orchestrates learning
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from src.utils.logging import get_logger


class SleepSystem:
    """
    Sistema de sono: Consolidação durante inatividade
    Detecta inatividade (30 minutos), extrai feedback, filtra positivo,
    orquestra processo de aprendizado
    """
    
    def __init__(
        self,
        storage,
        replay,
        fine_tuning,
        emotional_analyzer=None,
        implicit_feedback=None,
        inactivity_threshold_minutes: int = 30
    ):
        """
        Inicializa sistema de sono
        
        Args:
            storage: Sistema de armazenamento (PostgreSQL)
            replay: Sistema de replay
            fine_tuning: Sistema de fine-tuning
            emotional_analyzer: Analisador emocional (opcional)
            implicit_feedback: Sistema de feedback implícito (opcional)
            inactivity_threshold_minutes: Limite de inatividade em minutos
        """
        self.logger = get_logger(self.__class__.__name__)
        self.storage = storage
        self.replay = replay
        self.fine_tuning = fine_tuning
        self.emotional_analyzer = emotional_analyzer
        self.implicit_feedback = implicit_feedback
        self.inactivity_threshold = timedelta(minutes=inactivity_threshold_minutes)
        self.last_activity: Optional[datetime] = None
        self.logger.info(f"Sleep system initialized (threshold: {inactivity_threshold_minutes} minutes)")
    
    def record_activity(self):
        """Registra atividade do usuário"""
        self.last_activity = datetime.utcnow()
    
    def is_inactive(self) -> bool:
        """
        Verifica se sistema está inativo
        
        Returns:
            True se inativo por mais que o threshold
        """
        if self.last_activity is None:
            return False
        
        inactive_time = datetime.utcnow() - self.last_activity
        return inactive_time >= self.inactivity_threshold
    
    def consolidate(self) -> Dict[str, Any]:
        """
        Consolida conhecimento durante sono
        
        Processo:
        1. Detecta inatividade
        2. Extrai feedback do PostgreSQL
        3. Filtra apenas positivo (score > 0.7)
        4. Mistura exemplos antigos com novos (replay)
        5. Fine-tuning tradicional incremental
        6. Atualiza LoRA Adapters
        
        Returns:
            Dicionário com resultados da consolidação
        """
        if not self.is_inactive():
            return {
                "status": "active",
                "message": "System is still active, no consolidation needed"
            }
        
        self.logger.info("Starting sleep consolidation...")
        
        try:
            # 1. Extrai feedback do PostgreSQL
            all_feedbacks = self.storage.get_all_feedbacks()
            self.logger.info(f"Extracted {len(all_feedbacks)} feedbacks from storage")
            
            # 2. Filtra apenas positivo (score > 0.7)
            positive_feedbacks = [
                f for f in all_feedbacks
                if f.get('score', 0) > 0.7
            ]
            self.logger.info(f"Filtered {len(positive_feedbacks)} positive feedbacks")
            
            if len(positive_feedbacks) == 0:
                return {
                    "status": "no_data",
                    "message": "No positive feedbacks to consolidate"
                }
            
            # 3. Replay: mistura exemplos antigos com novos
            old_examples = self.storage.get_important_examples()
            dataset = self.replay.mix_examples(old_examples, positive_feedbacks)
            self.logger.info(f"Created dataset with {len(dataset)} examples (replay)")
            
            # 4. Fine-tuning tradicional incremental
            fine_tuning_result = self.fine_tuning.train_incremental(dataset)
            self.logger.info("Fine-tuning completed")
            
            # 5. Atualiza LoRA Adapters
            update_result = self.fine_tuning.update_adapters()
            self.logger.info("Adapters updated")
            
            return {
                "status": "success",
                "feedbacks_processed": len(positive_feedbacks),
                "dataset_size": len(dataset),
                "fine_tuning": fine_tuning_result,
                "adapters_updated": update_result
            }
        
        except Exception as e:
            self.logger.error(f"Error during sleep consolidation: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def trigger_manual(self) -> Dict[str, Any]:
        """
        Aciona consolidação manualmente (sem verificar inatividade)
        
        Returns:
            Resultado da consolidação
        """
        self.logger.info("Manual sleep consolidation triggered")
        return self.consolidate()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status do sistema de sono
        
        Returns:
            Dicionário com status
        """
        is_inactive = self.is_inactive()
        last_activity_str = self.last_activity.isoformat() if self.last_activity else None
        
        return {
            "status": "inactive" if is_inactive else "active",
            "last_activity": last_activity_str,
            "inactivity_threshold_minutes": self.inactivity_threshold.total_seconds() / 60
        }

