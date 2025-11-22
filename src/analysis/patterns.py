"""
Pattern Identification and Generalization
Identifies common patterns and generalizes them for multiple projects
"""

from typing import List, Dict, Any, Optional
from collections import defaultdict

from src.utils.logging import get_logger


class PatternIdentifier:
    """
    Identificador de padrões
    Identifica padrões comuns entre projetos e generaliza
    """
    
    def __init__(self):
        """Inicializa identificador de padrões"""
        self.logger = get_logger(self.__class__.__name__)
        self.patterns_db: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.logger.info("Pattern identifier initialized")
    
    def identify_common_patterns(
        self,
        project_analyses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Identifica padrões comuns entre múltiplos projetos
        
        Args:
            project_analyses: Lista de análises de projetos
        
        Returns:
            Lista de padrões comuns identificados
        """
        self.logger.info(f"Identifying common patterns from {len(project_analyses)} projects")
        
        # Agrupa padrões por tipo
        patterns_by_type = defaultdict(list)
        
        for analysis in project_analyses:
            patterns = analysis.get("patterns_found", [])
            for pattern in patterns:
                patterns_by_type[pattern].append(analysis["project_path"])
        
        # Identifica padrões que aparecem em múltiplos projetos
        common_patterns = []
        for pattern_type, projects in patterns_by_type.items():
            if len(projects) >= 2:  # Aparece em pelo menos 2 projetos
                common_patterns.append({
                    "pattern": pattern_type,
                    "frequency": len(projects),
                    "projects": projects,
                    "generalization": self._generalize_pattern(pattern_type, projects)
                })
        
        self.logger.info(f"Found {len(common_patterns)} common patterns")
        return common_patterns
    
    def _generalize_pattern(
        self,
        pattern_type: str,
        projects: List[str]
    ) -> Dict[str, Any]:
        """
        Generaliza padrão para conceito aplicável
        
        Args:
            pattern_type: Tipo do padrão
            projects: Lista de projetos onde aparece
        
        Returns:
            Generalização do padrão
        """
        generalizations = {
            "repository": {
                "concept": "Data access abstraction",
                "applicable_to": ["Python", "Java", "TypeScript", "Go"],
                "use_cases": ["Database access", "API integration", "File system"]
            },
            "factory": {
                "concept": "Object creation abstraction",
                "applicable_to": ["All languages"],
                "use_cases": ["Dependency injection", "Configuration", "Testing"]
            },
            "mvc": {
                "concept": "Separation of concerns",
                "applicable_to": ["Web frameworks", "Desktop applications"],
                "use_cases": ["User interfaces", "API design", "State management"]
            },
            "adapter": {
                "concept": "Interface compatibility",
                "applicable_to": ["All languages"],
                "use_cases": ["Legacy integration", "Third-party libraries", "API versioning"]
            }
        }
        
        return generalizations.get(pattern_type, {
            "concept": f"Pattern: {pattern_type}",
            "applicable_to": ["General"],
            "use_cases": ["Various"]
        })
    
    def extract_general_concepts(
        self,
        patterns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extrai conceitos gerais dos padrões
        
        Args:
            patterns: Lista de padrões identificados
        
        Returns:
            Lista de conceitos gerais
        """
        concepts = []
        
        for pattern in patterns:
            generalization = pattern.get("generalization", {})
            concept = generalization.get("concept", pattern["pattern"])
            
            # Evita duplicatas
            if not any(c["concept"] == concept for c in concepts):
                concepts.append({
                    "concept": concept,
                    "patterns": [pattern["pattern"]],
                    "applicable_to": generalization.get("applicable_to", []),
                    "use_cases": generalization.get("use_cases", [])
                })
            else:
                # Adiciona padrão ao conceito existente
                for c in concepts:
                    if c["concept"] == concept:
                        c["patterns"].append(pattern["pattern"])
                        break
        
        return concepts
    
    def consolidate_knowledge(
        self,
        patterns: List[Dict[str, Any]],
        feedback_scores: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Consolida conhecimento de padrões
        
        Args:
            patterns: Lista de padrões
            feedback_scores: Scores de feedback por padrão (opcional)
        
        Returns:
            Conhecimento consolidado
        """
        self.logger.info("Consolidating pattern knowledge")
        
        # Prioriza padrões com feedback positivo
        if feedback_scores:
            patterns = sorted(
                patterns,
                key=lambda p: feedback_scores.get(p["pattern"], 0.5),
                reverse=True
            )
        
        # Extrai conceitos gerais
        concepts = self.extract_general_concepts(patterns)
        
        # Consolida em conhecimento reutilizável
        consolidated = {
            "patterns": patterns,
            "concepts": concepts,
            "total_patterns": len(patterns),
            "total_concepts": len(concepts),
            "most_common": patterns[0]["pattern"] if patterns else None
        }
        
        return consolidated

