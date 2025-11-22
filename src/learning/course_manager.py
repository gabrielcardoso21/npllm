"""
Course Manager
Manages course lifecycle and status
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

from src.utils.logging import get_logger


class CourseStatus(Enum):
    """Status de um curso"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VALIDATED = "validated"
    ERROR = "error"


class CourseManager:
    """
    Gerenciador de cursos
    Gerencia ciclo de vida de cursos
    """
    
    def __init__(self, storage):
        """
        Inicializa gerenciador de cursos
        
        Args:
            storage: Instância de PostgreSQLStorage
        """
        self.logger = get_logger(self.__class__.__name__)
        self.storage = storage
        self.logger.info("Course manager initialized")
    
    def create_course(
        self,
        name: str,
        description: str,
        source_type: str,
        source_path: str
    ) -> Dict[str, Any]:
        """
        Cria um novo curso
        
        Args:
            name: Nome do curso
            description: Descrição do curso
            source_type: Tipo de fonte ('url', 'file', 'directory', 'text')
            source_path: Caminho/URL da fonte
        
        Returns:
            Dicionário com informações do curso criado
        """
        self.logger.info(f"Creating course: {name}")
        
        course_id = self.storage.store_course(
            name=name,
            description=description,
            source_type=source_type,
            source_path=source_path
        )
        
        course = {
            "id": course_id,
            "name": name,
            "description": description,
            "source_type": source_type,
            "source_path": source_path,
            "status": CourseStatus.NOT_STARTED.value,
            "created_at": datetime.now().isoformat()
        }
        
        self.logger.info(f"Course created with ID: {course_id}")
        return course
    
    def list_courses(self) -> List[Dict[str, Any]]:
        """
        Lista todos os cursos
        
        Returns:
            Lista de cursos
        """
        self.logger.info("Listing all courses")
        return self.storage.get_all_courses()
    
    def get_course_status(self, course_id: int) -> Dict[str, Any]:
        """
        Obtém status de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Status e informações do curso
        """
        course = self.storage.get_course(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        # Conta conteúdo processado
        content_count = self.storage.get_course_content_count(course_id)
        
        # Conta conceitos aprendidos
        concepts_count = self.storage.get_learned_concepts_count(course_id)
        
        return {
            "id": course["id"],
            "name": course["name"],
            "status": course["status"],
            "content_chunks": content_count,
            "concepts_learned": concepts_count,
            "created_at": course["created_at"],
            "updated_at": course.get("updated_at")
        }
    
    def start_course(self, course_id: int) -> Dict[str, Any]:
        """
        Inicia processamento de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Status da operação
        """
        self.logger.info(f"Starting course {course_id}")
        
        # Atualiza status para "in_progress"
        self.storage.update_course_status(course_id, CourseStatus.IN_PROGRESS.value)
        
        return {
            "status": "started",
            "course_id": course_id,
            "message": "Course processing started"
        }
    
    def validate_course(self, course_id: int) -> Dict[str, Any]:
        """
        Marca curso como validado manualmente
        
        Args:
            course_id: ID do curso
        
        Returns:
            Status da validação
        """
        self.logger.info(f"Validating course {course_id}")
        
        # Atualiza status para "validated"
        self.storage.update_course_status(course_id, CourseStatus.VALIDATED.value)
        
        return {
            "status": "validated",
            "course_id": course_id,
            "message": "Course marked as validated"
        }
    
    def update_course_status(
        self,
        course_id: int,
        status: CourseStatus
    ) -> Dict[str, Any]:
        """
        Atualiza status de um curso
        
        Args:
            course_id: ID do curso
            status: Novo status
        
        Returns:
            Status da atualização
        """
        self.logger.info(f"Updating course {course_id} status to {status.value}")
        self.storage.update_course_status(course_id, status.value)
        
        return {
            "status": "updated",
            "course_id": course_id,
            "new_status": status.value
        }

