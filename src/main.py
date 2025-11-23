"""
Main entry point for npllm
Simplified initialization based on new architecture
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

from src.models.base_model import CodeLlamaBaseModel
from src.adapters.selector import AdapterSelector
from src.adapters.manager import AdapterManager
from src.storage.postgres import PostgreSQLStorage
from src.feedback.emotional import EmotionalAnalyzer
from src.feedback.implicit import ImplicitFeedback, UserAction
from src.learning.sleep import SleepSystem
from src.learning.replay import ReplaySystem
from src.learning.fine_tuning import FineTuningSystem
from src.analysis.architecture import ArchitectureAnalyzer
from src.analysis.patterns import PatternIdentifier
from src.transfer.learning import TransferLearning
from src.generation.architectural import ArchitecturalGenerator
from src.learning.course_manager import CourseManager, CourseStatus
from src.data_collection.content_collector import ContentCollector
from src.learning.content_processor import ContentProcessor
from src.learning.course_learner import CourseLearner
from src.learning.course_validator import CourseValidator

from src.utils.config import get_config
from src.utils.logging import get_logger


class NpllmSystem:
    """
    Sistema npllm simplificado
    Integra todos os componentes essenciais
    """
    
    def __init__(self, config_path: str = None):
        """
        Inicializa sistema completo
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.logger = get_logger("npllm")
        self.config = get_config(config_path)
        
        self.logger.info("Initializing npllm system (new architecture)...")
        
        # 1. LLM Base (não treina)
        self.logger.info("Loading base model...")
        self.base_model = CodeLlamaBaseModel()
        
        # 2. Seletor de Adapter (não treina)
        self.logger.info("Initializing adapter selector...")
        self.selector = AdapterSelector()
        
        # 3. Adapter Manager
        self.logger.info("Initializing adapter manager...")
        self.adapter_manager = AdapterManager(self.base_model)
        
        # 4. PostgreSQL Storage
        self.logger.info("Initializing PostgreSQL storage...")
        self.storage = PostgreSQLStorage()
        
        # 5. Análise Emocional
        self.logger.info("Initializing emotional analyzer...")
        self.emotional_analyzer = EmotionalAnalyzer()
        
        # 6. Feedback Implícito
        self.logger.info("Initializing implicit feedback...")
        self.implicit_feedback = ImplicitFeedback()
        
        # 7. Sistema de Replay
        self.logger.info("Initializing replay system...")
        self.replay = ReplaySystem()
        
        # 8. Sistema de Fine-tuning
        self.logger.info("Initializing fine-tuning system...")
        self.fine_tuning = FineTuningSystem(self.adapter_manager)
        
        # 9. Sistema de Sono
        self.logger.info("Initializing sleep system...")
        self.sleep = SleepSystem(
            storage=self.storage,
            replay=self.replay,
            fine_tuning=self.fine_tuning,
            emotional_analyzer=self.emotional_analyzer,
            implicit_feedback=self.implicit_feedback
        )
        
        # 10. Análise Arquitetural
        self.logger.info("Initializing architecture analyzer...")
        self.architecture_analyzer = ArchitectureAnalyzer()
        
        # 11. Identificação de Padrões
        self.logger.info("Initializing pattern identifier...")
        self.pattern_identifier = PatternIdentifier()
        
        # 12. Transfer Learning
        self.logger.info("Initializing transfer learning...")
        self.transfer_learning = TransferLearning(self.storage)
        
        # 13. Geração Arquitetural
        self.logger.info("Initializing architectural generator...")
        self.generator = ArchitecturalGenerator(self.base_model)
        
        # 14. Sistema de Cursos
        self.logger.info("Initializing course system...")
        self.course_manager = CourseManager(self.storage)
        self.content_collector = ContentCollector()
        self.content_processor = ContentProcessor()
        self.course_learner = CourseLearner(self.base_model, self.storage)
        self.course_validator = CourseValidator(self.base_model, self.storage, self.content_processor)
        
        self.logger.info("npllm system initialized successfully")
    
    def process_query(
        self,
        query: str,
        project_path: str = None,
        file_path: str = None
    ) -> Dict[str, Any]:
        """
        Processa query do usuário
        
        Fluxo simplificado:
        1. Usuário → LLM Base
        2. LLM Base → Seletor → Adapter
        3. Adapter → Resposta Final
        4. Resposta → Feedback → PostgreSQL
        
        Args:
            query: Query do usuário
            project_path: Caminho do projeto (opcional)
            file_path: Caminho do arquivo (opcional)
        
        Returns:
            Resposta com metadados
        """
        self.logger.info(f"Processing query: {query[:50]}...")
        
        # Registra atividade (para sistema de sono)
        self.sleep.record_activity()
        
        # 1. LLM Base processa (inferência apenas)
        # IMPORTANTE: stream=False para garantir retorno de string, não generator
        self.logger.info(f"Calling base_model.generate() with stream=False")
        response_raw = self.base_model.generate(query, max_length=8192, stream=False)
        self.logger.info(f"base_model.generate() returned type: {type(response_raw)}, is_string: {isinstance(response_raw, str)}")
        
        if not isinstance(response_raw, str):
            self.logger.error(f"ERROR: response_raw is not string! Type: {type(response_raw)}, value: {response_raw}")
            # Força conversão para string
            response_raw = str(response_raw) if response_raw else ""
        
        # 2. Seletor escolhe adapter
        project_structure = None
        if project_path:
            project_structure = {"path": project_path}
        
        adapter_name = self.selector.select(file_path=file_path, project_structure=project_structure)
        
        # 3. Adapter revisa resposta (se disponível)
        adapter = self.adapter_manager.get_adapter(adapter_name, prefer_stable=True)
        if adapter:
            # Adapter revisa resposta (simplificado - em produção, integração melhor)
            # Por enquanto, usa resposta bruta (adapter será aplicado durante fine-tuning)
            response = response_raw
        else:
            response = response_raw
        
        # Armazena adapter_name para feedback
        self._last_adapter_name = adapter_name
        
        # 4. Retorna resposta
        result = {
            "response": response,
            "adapter_used": adapter_name,
            "raw_response": response_raw
        }
        
        return result
    
    def capture_feedback(
        self,
        query: str,
        response: str,
        user_reaction: str,
        user_action: Optional[UserAction] = None,
        explicit_feedback: Optional[float] = None
    ):
        """
        Captura feedback do usuário
        
        Integra 70% implícito + 30% emocional
        
        Args:
            response: Resposta gerada
            user_reaction: Reação do usuário (texto)
            user_action: Ação do usuário (aceitar/editar/deletar)
            explicit_feedback: Feedback explícito (opcional)
        """
        self.logger.info("Capturing user feedback...")
        
        # 1. Análise emocional
        emotion_analysis = self.emotional_analyzer.analyze(user_reaction)
        emotional_score = emotion_analysis.get("signal", 0.0)
        
        # Prioriza feedback explícito se disponível
        if explicit_feedback is not None:
            emotional_score = explicit_feedback
        
        # 2. Feedback implícito
        implicit_score = 0.0
        if user_action:
            implicit_score = self.implicit_feedback.calculate_reward(user_action)
        
        # 3. Integração 70% implícito + 30% emocional
        total_score = 0.7 * implicit_score + 0.3 * emotional_score
        
        # 4. Armazena no PostgreSQL (direto, sem buffer)
        adapter_name = getattr(self, '_last_adapter_name', None)
        self.storage.store_feedback(
            prompt=query,  # Prompt original
            response=response,
            score=total_score,
            implicit_score=implicit_score,
            emotional_score=emotional_score,
            context=adapter_name
        )
        
        self.logger.info(f"Feedback stored (score: {total_score:.2f})")
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analisa projeto arquiteturalmente
        
        Args:
            project_path: Caminho do projeto
        
        Returns:
            Análise arquitetural
        """
        return self.architecture_analyzer.analyze_project(project_path)
    
    def suggest_architecture(self, project_path: str) -> Dict[str, Any]:
        """
        Sugere arquitetura para novo projeto
        
        Args:
            project_path: Caminho do projeto
        
        Returns:
            Sugestão de arquitetura
        """
        # Obtém padrões aprendidos
        # TODO: Buscar padrões do storage
        
        # Por enquanto, retorna sugestão básica
        return self.transfer_learning.suggest_architecture(
            project_path,
            []  # TODO: Padrões aprendidos
        )
    
    def trigger_sleep(self, force: bool = False):
        """
        Aciona consolidação manualmente (sono)
        
        Args:
            force: Se True, força consolidação mesmo se sistema estiver ativo
        """
        self.logger.info("Triggering sleep consolidation...")
        if force:
            return self.sleep.trigger_manual()
        else:
            return self.sleep.consolidate()
    
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
        return self.course_manager.create_course(name, description, source_type, source_path)
    
    def list_courses(self) -> List[Dict[str, Any]]:
        """
        Lista todos os cursos
        
        Returns:
            Lista de cursos
        """
        return self.course_manager.list_courses()
    
    def start_course_learning(self, course_id: int) -> Dict[str, Any]:
        """
        Inicia aprendizado de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Resultado do aprendizado
        """
        self.logger.info(f"Starting course learning for course {course_id}")
        
        # Atualiza status
        self.course_manager.start_course(course_id)
        
        # Obtém curso
        course = self.storage.get_course(course_id)
        if not course:
            raise ValueError(f"Course {course_id} not found")
        
        # Coleta conteúdo
        self.logger.info(f"Collecting content from {course['source_type']}: {course['source_path']}")
        
        if course['source_type'] == 'url':
            documents = self.content_collector.collect_from_url(course['source_path'])
        elif course['source_type'] == 'file':
            documents = self.content_collector.collect_from_file(course['source_path'])
        elif course['source_type'] == 'directory':
            documents = self.content_collector.collect_from_directory(course['source_path'])
        elif course['source_type'] == 'text':
            documents = self.content_collector.collect_from_text(course['source_path'])
        else:
            raise ValueError(f"Unknown source type: {course['source_type']}")
        
        # Processa e armazena conteúdo
        total_chunks = 0
        for doc in documents:
            processed_chunks = self.content_processor.process_content(
                content=doc['content'],
                course_id=course_id,
                metadata={
                    'title': doc.get('title', ''),
                    'type': doc.get('type', 'unknown'),
                    'url': doc.get('url'),
                    'file_path': doc.get('file_path')
                }
            )
            
            # Armazena cada chunk
            for chunk in processed_chunks:
                self.storage.store_course_content(
                    course_id=course_id,
                    title=chunk['metadata'].get('title', ''),
                    content=chunk['content'],
                    chunk_index=chunk['chunk_index'],
                    metadata=chunk['metadata'],
                    embedding=chunk['embedding']
                )
                total_chunks += 1
        
        self.logger.info(f"Stored {total_chunks} content chunks")
        
        # Aprende padrões e conceitos
        learning_result = self.course_learner.learn_from_course(course_id)
        
        # Atualiza status para concluído
        self.course_manager.update_course_status(course_id, CourseStatus.COMPLETED)
        
        return {
            "status": "success",
            "course_id": course_id,
            "documents_collected": len(documents),
            "chunks_stored": total_chunks,
            "learning": learning_result
        }
    
    def get_course_status(self, course_id: int) -> Dict[str, Any]:
        """
        Obtém status de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Status do curso
        """
        return self.course_manager.get_course_status(course_id)
    
    def get_course_concepts(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Obtém conceitos aprendidos de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Lista de conceitos aprendidos
        """
        return self.course_learner.get_learned_concepts(course_id)
    
    def validate_course(
        self,
        course_id: int,
        automatic: bool = False,
        num_questions: int = 10,
        validation_threshold: float = 0.75
    ) -> Dict[str, Any]:
        """
        Valida um curso (manual ou automático)
        
        Args:
            course_id: ID do curso
            automatic: Se True, valida automaticamente. Se False, marca como validado manualmente
            num_questions: Número de perguntas para validação automática
            validation_threshold: Threshold mínimo para validação automática (0.0 a 1.0)
        
        Returns:
            Resultado da validação
        """
        if automatic:
            # Validação automática
            self.logger.info(f"Starting automatic validation for course {course_id}")
            validation_result = self.course_validator.validate_course(
                course_id,
                num_questions=num_questions,
                validation_threshold=validation_threshold
            )
            
            # Se passou, marca como validado
            if validation_result.get('passed', False):
                self.course_manager.validate_course(course_id)
                validation_result['auto_validated'] = True
            else:
                validation_result['auto_validated'] = False
            
            return validation_result
        else:
            # Validação manual (apenas marca como validado)
            return self.course_manager.validate_course(course_id)
    
    def process_query(
        self,
        query: str,
        project_path: str = None,
        file_path: str = None,
        course_context: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Processa query do usuário
        
        Fluxo simplificado:
        1. Usuário → LLM Base
        2. LLM Base → Seletor → Adapter
        3. Adapter → Resposta Final
        4. Resposta → Feedback → PostgreSQL
        
        Args:
            query: Query do usuário
            project_path: Caminho do projeto (opcional)
            file_path: Caminho do arquivo (opcional)
            course_context: ID do curso para contexto (opcional)
        
        Returns:
            Resposta com metadados
        """
        self.logger.info(f"Processing query: {query[:50]}...")
        
        # Registra atividade (para sistema de sono)
        self.sleep.record_activity()
        
        # Se course_context fornecido, busca conteúdo relevante
        context_content = ""
        if course_context:
            try:
                # Gera embedding da query
                query_embedding = self.content_processor.generate_embedding(query)
                
                # Busca conteúdo relevante do curso
                relevant_chunks = self.storage.search_course_content(
                    course_context,
                    query_embedding,
                    top_k=3
                )
                
                # Adiciona contexto à query
                if relevant_chunks:
                    context_content = "\n\nRelevant context from course:\n"
                    for chunk in relevant_chunks:
                        context_content += f"- {chunk['title']}: {chunk['content'][:200]}...\n"
                    
                    query = f"{context_content}\n\nUser query: {query}"
            except Exception as e:
                self.logger.warning(f"Error retrieving course context: {e}")
        
        # 1. LLM Base processa (inferência apenas)
        # IMPORTANTE: stream=False para garantir retorno de string, não generator
        self.logger.info(f"Calling base_model.generate() with stream=False")
        response_raw = self.base_model.generate(query, max_length=8192, stream=False)
        self.logger.info(f"base_model.generate() returned type: {type(response_raw)}, is_string: {isinstance(response_raw, str)}")
        
        if not isinstance(response_raw, str):
            self.logger.error(f"ERROR: response_raw is not string! Type: {type(response_raw)}, value: {response_raw}")
            # Força conversão para string
            response_raw = str(response_raw) if response_raw else ""
        
        # 2. Seletor escolhe adapter
        project_structure = None
        if project_path:
            project_structure = {"path": project_path}
        
        adapter_name = self.selector.select(file_path=file_path, project_structure=project_structure)
        
        # 3. Adapter revisa resposta (se disponível)
        adapter = self.adapter_manager.get_adapter(adapter_name, prefer_stable=True)
        if adapter:
            # Adapter revisa resposta (simplificado - em produção, integração melhor)
            # Por enquanto, usa resposta bruta (adapter será aplicado durante fine-tuning)
            response = response_raw
        else:
            response = response_raw
        
        # Armazena adapter_name para feedback
        self._last_adapter_name = adapter_name
        
        # 4. Retorna resposta
        result = {
            "response": response,
            "adapter_used": adapter_name,
            "raw_response": response_raw,
            "course_context_used": course_context is not None
        }
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Retorna status do sistema
        """
        return {
            "health": {
                "healthy": True,
                "warnings": []
            },
            "sleep_system": self.sleep.get_status(),
            "storage_status": "connected" if self.storage else "disconnected",
            "courses_count": len(self.list_courses())
        }
    
    def close(self):
        """Fecha sistema"""
        self.logger.info("Closing npllm system...")
        if hasattr(self, 'storage') and self.storage:
            self.storage.close()
        if hasattr(self, 'base_model') and self.base_model:
            self.base_model.unload_model()
        self.logger.info("System closed")


def initialize_system(config_path: str = None):
    """
    Inicializa sistema completo
    
    Args:
        config_path: Caminho para arquivo de configuração
    
    Returns:
        Sistema inicializado
    """
    return NpllmSystem(config_path)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="NeuroPlastic Large Language Model")
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Process a single query"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=None,
        help="Path to project"
    )
    parser.add_argument(
        "--analyze",
        type=str,
        default=None,
        help="Analyze project architecture"
    )
    parser.add_argument(
        "--sleep",
        action="store_true",
        help="Trigger sleep consolidation"
    )
    
    args = parser.parse_args()
    
    # Inicializa sistema
    system = initialize_system(args.config)
    
    try:
        if args.analyze:
            # Analisa projeto
            analysis = system.analyze_project(args.analyze)
            print(f"Analysis complete for: {args.analyze}")
            print(f"Patterns found: {analysis.get('patterns_found', [])}")
        
        elif args.sleep:
            # Aciona sono
            result = system.trigger_sleep()
            print(f"Sleep consolidation: {result.get('status', 'unknown')}")
        
        elif args.query:
            # Processa query
            result = system.process_query(
                query=args.query,
                project_path=args.project_path
            )
            print(f"Response: {result['response']}")
            print(f"Adapter used: {result['adapter_used']}")
        
        else:
            # Modo interativo básico
            print("npllm system (new architecture)")
            print("Use --query to process queries")
            print("Use --analyze to analyze projects")
            print("Use --sleep to trigger consolidation")
            print("Press Ctrl+C to stop.")
            
            import time
            while True:
                time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping system...")
    finally:
        system.close()


if __name__ == "__main__":
    main()
