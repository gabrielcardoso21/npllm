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
            
            # Adiciona exemplos de cursos validados
            course_examples = self._get_course_examples()
            if course_examples:
                self.logger.info(f"Adding {len(course_examples)} examples from validated courses")
                old_examples.extend(course_examples)
            
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
    
    def _get_course_examples(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Obtém exemplos de cursos validados para uso no replay
        
        Args:
            limit: Número máximo de exemplos
        
        Returns:
            Lista de exemplos de cursos
        """
        try:
            # Obtém todos os cursos validados
            all_courses = self.storage.get_all_courses()
            validated_courses = [
                c for c in all_courses
                if c.get('status') == 'validated'
            ]
            
            # Coleta exemplos de cada curso
            course_examples = []
            for course in validated_courses:
                examples = self.storage.get_course_examples_for_replay(
                    course['id'],
                    limit=limit // len(validated_courses) if validated_courses else limit
                )
                course_examples.extend(examples)
            
            return course_examples[:limit]
        
        except Exception as e:
            self.logger.warning(f"Error getting course examples: {e}")
            return []
    
    def consolidate_course_knowledge(self, course_id: int) -> Dict[str, Any]:
        """
        Consolida conhecimento de um curso específico durante o sono
        
        Args:
            course_id: ID do curso
        
        Returns:
            Resultado da consolidação
        """
        self.logger.info(f"Consolidating knowledge from course {course_id}")
        
        try:
            # Obtém exemplos do curso
            course_examples = self.storage.get_course_examples_for_replay(course_id, limit=100)
            
            if not course_examples:
                return {
                    "status": "no_data",
                    "message": f"No examples found for course {course_id}"
                }
            
            # Mistura com exemplos antigos
            old_examples = self.storage.get_important_examples()
            dataset = self.replay.mix_examples(old_examples, course_examples)
            
            # Fine-tuning
            fine_tuning_result = self.fine_tuning.train_incremental(dataset)
            update_result = self.fine_tuning.update_adapters()
            
            return {
                "status": "success",
                "course_id": course_id,
                "examples_processed": len(course_examples),
                "dataset_size": len(dataset),
                "fine_tuning": fine_tuning_result,
                "adapters_updated": update_result
            }
        
        except Exception as e:
            self.logger.error(f"Error consolidating course knowledge: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
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

