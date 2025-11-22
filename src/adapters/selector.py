"""
Simple adapter selector based on context (file extension, project structure)
No training needed - just heuristics
"""

from typing import Optional, Dict
from pathlib import Path
from src.utils.logging import get_logger


class AdapterSelector:
    """
    Seletor simples de adapter baseado em contexto
    Usa heurísticas (extensão de arquivo, estrutura de projeto)
    Não precisa treinar
    """
    
    def __init__(self):
        """Inicializa seletor"""
        self.logger = get_logger(self.__class__.__name__)
        
        # Mapeamento de extensões para adapters
        self.extension_map = {
            '.py': 'python_adapter',
            '.js': 'javascript_adapter',
            '.ts': 'typescript_adapter',
            '.java': 'java_adapter',
            '.go': 'go_adapter',
            '.rs': 'rust_adapter',
            '.cpp': 'cpp_adapter',
            '.c': 'c_adapter',
        }
        
        # Mapeamento de estruturas de projeto para adapters
        self.project_structure_map = {
            'odoo': 'odoo_adapter',
            'django': 'django_adapter',
            'react': 'react_adapter',
            'vue': 'vue_adapter',
            'angular': 'angular_adapter',
            'flask': 'flask_adapter',
            'fastapi': 'fastapi_adapter',
        }
        
        self.logger.info("Adapter selector initialized")
    
    def select(
        self,
        file_path: Optional[str] = None,
        project_structure: Optional[Dict] = None
    ) -> str:
        """
        Seleciona adapter baseado em contexto
        
        Args:
            file_path: Caminho do arquivo (para detectar extensão)
            project_structure: Estrutura do projeto (dict com informações)
        
        Returns:
            Nome do adapter selecionado
        """
        # 1. Por extensão de arquivo
        if file_path:
            path = Path(file_path)
            extension = path.suffix.lower()
            
            if extension in self.extension_map:
                adapter = self.extension_map[extension]
                self.logger.debug(f"Selected adapter by extension: {adapter}")
                return adapter
        
        # 2. Por estrutura de projeto
        if project_structure:
            # Verifica se algum padrão de projeto está presente
            project_path = project_structure.get('path', '')
            project_name = project_structure.get('name', '').lower()
            
            # Verifica no caminho
            for key, adapter in self.project_structure_map.items():
                if key in project_path.lower() or key in project_name:
                    self.logger.debug(f"Selected adapter by project structure: {adapter}")
                    return adapter
        
        # 3. Fallback para adapter genérico
        self.logger.debug("Using generic adapter (fallback)")
        return 'generic_adapter'

