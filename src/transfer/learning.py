"""
Transfer Learning
Applies learned patterns from one project to another
"""

from typing import List, Dict, Any, Optional
import numpy as np

from src.utils.logging import get_logger


class TransferLearning:
    """
    Transfer Learning
    Aplica padrões aprendidos de um projeto em outro
    """
    
    def __init__(self, storage, embedding_provider=None):
        """
        Inicializa transfer learning
        
        Args:
            storage: Sistema de armazenamento (PostgreSQL)
            embedding_provider: Provedor de embeddings (opcional)
        """
        self.logger = get_logger(self.__class__.__name__)
        self.storage = storage
        self.embedding_provider = embedding_provider
        self.logger.info("Transfer learning initialized")
    
    def find_similar_projects(
        self,
        target_project_path: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Encontra projetos similares ao alvo
        
        Args:
            target_project_path: Caminho do projeto alvo
            top_k: Número de projetos similares
        
        Returns:
            Lista de projetos similares
        """
        self.logger.info(f"Finding similar projects to: {target_project_path}")
        
        # TODO: Implementar busca semântica de projetos
        # Por enquanto, retorna lista vazia
        # Em produção, usaria embeddings de estrutura de projeto
        
        return []
    
    def apply_patterns(
        self,
        source_patterns: List[Dict[str, Any]],
        target_project_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Aplica padrões aprendidos ao projeto alvo
        
        Args:
            source_patterns: Padrões aprendidos de projetos fonte
            target_project_structure: Estrutura do projeto alvo
        
        Returns:
            Lista de padrões aplicados com adaptações
        """
        self.logger.info(f"Applying {len(source_patterns)} patterns to target project")
        
        applied_patterns = []
        
        for pattern in source_patterns:
            # Verifica se padrão é aplicável
            if self._is_applicable(pattern, target_project_structure):
                adapted = self._adapt_pattern(pattern, target_project_structure)
                applied_patterns.append(adapted)
        
        self.logger.info(f"Applied {len(applied_patterns)} patterns")
        return applied_patterns
    
    def _is_applicable(
        self,
        pattern: Dict[str, Any],
        target_structure: Dict[str, Any]
    ) -> bool:
        """
        Verifica se padrão é aplicável ao projeto alvo
        
        Args:
            pattern: Padrão a verificar
            target_structure: Estrutura do projeto alvo
        
        Returns:
            True se aplicável
        """
        generalization = pattern.get("generalization", {})
        applicable_to = generalization.get("applicable_to", [])
        
        # Verifica se estrutura do projeto é compatível
        # Por enquanto, sempre retorna True (simplificado)
        return True
    
    def _adapt_pattern(
        self,
        pattern: Dict[str, Any],
        target_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adapta padrão ao contexto do projeto alvo
        
        Args:
            pattern: Padrão original
            target_structure: Estrutura do projeto alvo
        
        Returns:
            Padrão adaptado
        """
        adapted = {
            "pattern": pattern["pattern"],
            "original_projects": pattern.get("projects", []),
            "adapted_for": target_structure.get("project_path", "unknown"),
            "adaptations": self._generate_adaptations(pattern, target_structure)
        }
        
        return adapted
    
    def _generate_adaptations(
        self,
        pattern: Dict[str, Any],
        target_structure: Dict[str, Any]
    ) -> List[str]:
        """
        Gera sugestões de adaptação
        
        Args:
            pattern: Padrão original
            target_structure: Estrutura do projeto alvo
        
        Returns:
            Lista de sugestões de adaptação
        """
        adaptations = []
        
        pattern_type = pattern["pattern"]
        
        if pattern_type == "repository":
            adaptations.append("Create repository interface in models/ or data/ directory")
            adaptations.append("Implement repository with database access")
        
        elif pattern_type == "factory":
            adaptations.append("Create factory class in utils/ or factories/ directory")
            adaptations.append("Implement factory methods for object creation")
        
        elif pattern_type == "mvc":
            adaptations.append("Organize code into controllers/, models/, views/ directories")
            adaptations.append("Separate business logic from presentation")
        
        return adaptations
    
    def suggest_architecture(
        self,
        target_project_path: str,
        learned_patterns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Sugere arquitetura para novo projeto baseado em padrões aprendidos
        
        Args:
            target_project_path: Caminho do projeto alvo
            learned_patterns: Padrões aprendidos
        
        Returns:
            Sugestão de arquitetura
        """
        self.logger.info(f"Suggesting architecture for: {target_project_path}")
        
        # Prioriza padrões com maior frequência e feedback positivo
        sorted_patterns = sorted(
            learned_patterns,
            key=lambda p: p.get("frequency", 0) * p.get("score", 0.5),
            reverse=True
        )
        
        # Seleciona top padrões
        top_patterns = sorted_patterns[:5]
        
        # Gera sugestão de estrutura
        suggestion = {
            "project_path": target_project_path,
            "recommended_patterns": [p["pattern"] for p in top_patterns],
            "suggested_structure": self._generate_structure_suggestion(top_patterns),
            "rationale": "Based on successful patterns from similar projects"
        }
        
        return suggestion
    
    def _generate_structure_suggestion(
        self,
        patterns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Gera sugestão de estrutura de diretórios
        
        Args:
            patterns: Padrões recomendados
        
        Returns:
            Sugestão de estrutura
        """
        structure = {}
        
        for pattern in patterns:
            pattern_type = pattern["pattern"]
            
            if pattern_type == "mvc":
                structure["controllers"] = "Handle HTTP requests and business logic"
                structure["models"] = "Domain models and data structures"
                structure["views"] = "Presentation layer (templates, components)"
            
            elif pattern_type == "repository":
                structure["repositories"] = "Data access layer"
                structure["models"] = "Domain models"
            
            elif pattern_type == "factory":
                structure["factories"] = "Object creation and dependency injection"
        
        return structure

