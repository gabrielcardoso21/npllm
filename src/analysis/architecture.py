"""
Architectural Analysis
Analyzes project structure and extracts architectural patterns
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast
import re

from src.utils.logging import get_logger


class ArchitectureAnalyzer:
    """
    Analisador arquitetural
    Analisa estrutura de projetos e extrai padrões arquiteturais
    """
    
    def __init__(self):
        """Inicializa analisador arquitetural"""
        self.logger = get_logger(self.__class__.__name__)
        
        # Padrões de design conhecidos
        self.design_patterns = {
            "repository": [
                r"class\s+\w+Repository",
                r"def\s+find_by",
                r"def\s+save",
                r"def\s+delete"
            ],
            "factory": [
                r"class\s+\w+Factory",
                r"def\s+create",
                r"def\s+get_instance"
            ],
            "singleton": [
                r"class\s+\w+.*:\s*$",
                r"_instance\s*=",
                r"def\s+__new__"
            ],
            "observer": [
                r"def\s+attach",
                r"def\s+detach",
                r"def\s+notify"
            ],
            "strategy": [
                r"class\s+\w+Strategy",
                r"def\s+execute",
                r"def\s+algorithm"
            ],
            "mvc": [
                r"class\s+\w+Controller",
                r"class\s+\w+Model",
                r"class\s+\w+View"
            ],
            "adapter": [
                r"class\s+\w+Adapter",
                r"def\s+adapt",
                r"def\s+convert"
            ]
        }
        
        self.logger.info("Architecture analyzer initialized")
    
    def parse_directory_structure(self, project_path: str) -> Dict[str, Any]:
        """
        Analisa estrutura de diretórios do projeto
        
        Args:
            project_path: Caminho do projeto
        
        Returns:
            Dicionário com estrutura de diretórios
        """
        self.logger.info(f"Parsing directory structure: {project_path}")
        
        structure = {}
        path = Path(project_path)
        
        if not path.exists():
            self.logger.warning(f"Path does not exist: {project_path}")
            return structure
        
        def _parse_dir(directory: Path, depth: int = 0, max_depth: int = 5) -> Dict:
            """Recursivamente parseia diretório"""
            if depth > max_depth:
                return {}
            
            dir_structure = {}
            
            try:
                for item in directory.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        # Ignora diretórios comuns
                        if item.name in ['__pycache__', '.git', 'node_modules', '.venv', 'venv']:
                            continue
                        
                        dir_structure[item.name] = _parse_dir(item, depth + 1, max_depth)
                    
                    elif item.is_file() and item.suffix in ['.py', '.js', '.ts', '.java', '.go']:
                        # Conta arquivos por tipo
                        suffix = item.suffix[1:]  # Remove o ponto
                        if suffix not in dir_structure:
                            dir_structure[suffix] = []
                        dir_structure[suffix].append(item.name)
            
            except PermissionError:
                self.logger.warning(f"Permission denied: {directory}")
            
            return dir_structure
        
        structure = _parse_dir(path)
        self.logger.info(f"Parsed structure with {len(structure)} top-level items")
        
        return structure
    
    def identify_design_patterns(self, code: str) -> List[str]:
        """
        Identifica padrões de design no código
        
        Args:
            code: Código fonte
        
        Returns:
            Lista de padrões identificados
        """
        patterns_found = []
        
        for pattern_name, pattern_regexes in self.design_patterns.items():
            matches = 0
            for regex in pattern_regexes:
                if re.search(regex, code, re.MULTILINE | re.IGNORECASE):
                    matches += 1
            
            # Se encontrou pelo menos metade dos padrões, considera identificado
            if matches >= len(pattern_regexes) / 2:
                patterns_found.append(pattern_name)
                self.logger.debug(f"Found pattern: {pattern_name}")
        
        return patterns_found
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analisa um arquivo individual
        
        Args:
            file_path: Caminho do arquivo
        
        Returns:
            Dicionário com análise do arquivo
        """
        path = Path(file_path)
        
        if not path.exists():
            return {}
        
        analysis = {
            "file_path": str(path),
            "file_name": path.name,
            "extension": path.suffix,
            "patterns": [],
            "classes": [],
            "functions": []
        }
        
        if path.suffix == '.py':
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Identifica padrões
                analysis["patterns"] = self.identify_design_patterns(code)
                
                # Parseia AST para classes e funções
                try:
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            analysis["classes"].append(node.name)
                        elif isinstance(node, ast.FunctionDef):
                            analysis["functions"].append(node.name)
                except SyntaxError:
                    self.logger.warning(f"Syntax error in {file_path}")
            
            except Exception as e:
                self.logger.error(f"Error analyzing file {file_path}: {e}")
        
        return analysis
    
    def extract_architectural_decisions(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai decisões arquiteturais da estrutura
        
        Args:
            structure: Estrutura de diretórios
        
        Returns:
            Lista de decisões arquiteturais
        """
        decisions = []
        
        # Analisa organização de diretórios
        if "src" in structure or "lib" in structure:
            decisions.append({
                "type": "directory_organization",
                "decision": "Source code organized in src/lib directory",
                "rationale": "Standard project structure"
            })
        
        if "tests" in structure or "test" in structure:
            decisions.append({
                "type": "testing",
                "decision": "Separate test directory",
                "rationale": "Test code separated from source"
            })
        
        # Analisa padrões de nomenclatura
        if "models" in structure.get("src", {}):
            decisions.append({
                "type": "separation_of_concerns",
                "decision": "Models separated from other components",
                "rationale": "Domain models isolated"
            })
        
        if "adapters" in structure.get("src", {}):
            decisions.append({
                "type": "adapter_pattern",
                "decision": "Adapters used for external integrations",
                "rationale": "Adapter pattern for flexibility"
            })
        
        return decisions
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analisa projeto completo
        
        Args:
            project_path: Caminho do projeto
        
        Returns:
            Dicionário com análise completa
        """
        self.logger.info(f"Analyzing project: {project_path}")
        
        # 1. Parseia estrutura
        structure = self.parse_directory_structure(project_path)
        
        # 2. Extrai decisões arquiteturais
        decisions = self.extract_architectural_decisions(structure)
        
        # 3. Analisa arquivos principais
        path = Path(project_path)
        main_files = []
        
        if path.exists():
            # Encontra arquivos principais (main.py, app.py, index.js, etc.)
            for pattern in ["main.py", "app.py", "index.py", "index.js", "index.ts"]:
                file_path = path / pattern
                if file_path.exists():
                    main_files.append(self.analyze_file(str(file_path)))
        
        return {
            "project_path": project_path,
            "structure": structure,
            "architectural_decisions": decisions,
            "main_files": main_files,
            "patterns_found": list(set(
                pattern
                for file_analysis in main_files
                for pattern in file_analysis.get("patterns", [])
            ))
        }

