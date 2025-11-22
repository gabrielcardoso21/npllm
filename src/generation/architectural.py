"""
Architectural Code Generation
Generates code that implements architectural decisions
"""

from typing import Dict, List, Any, Optional
from pathlib import Path

from src.utils.logging import get_logger


class ArchitecturalGenerator:
    """
    Gerador de código arquitetural
    Gera código que implementa decisões arquiteturais
    """
    
    def __init__(self, llm):
        """
        Inicializa gerador arquitetural
        
        Args:
            llm: Modelo LLM para geração
        """
        self.logger = get_logger(self.__class__.__name__)
        self.llm = llm
        
        # Templates arquiteturais
        self.templates = {
            "repository": {
                "python": """
class {name}Repository:
    \"\"\"Repository for {name} entities\"\"\"
    
    def __init__(self, db):
        self.db = db
    
    def find_by_id(self, id):
        return self.db.query({name}).filter_by(id=id).first()
    
    def find_all(self):
        return self.db.query({name}).all()
    
    def save(self, entity):
        self.db.add(entity)
        self.db.commit()
        return entity
    
    def delete(self, entity):
        self.db.delete(entity)
        self.db.commit()
""",
                "typescript": """
export class {name}Repository {{
    constructor(private db: Database) {{}}
    
    async findById(id: string): Promise<{name} | null> {{
        return await this.db.query('SELECT * FROM {table} WHERE id = $1', [id]);
    }}
    
    async findAll(): Promise<{name}[]> {{
        return await this.db.query('SELECT * FROM {table}');
    }}
    
    async save(entity: {name}): Promise<{name}> {{
        // Implementation
        return entity;
    }}
}}
"""
            },
            "factory": {
                "python": """
class {name}Factory:
    \"\"\"Factory for creating {name} instances\"\"\"
    
    @staticmethod
    def create(config: dict):
        return {name}(**config)
    
    @staticmethod
    def create_default():
        return {name}()
""",
                "typescript": """
export class {name}Factory {{
    static create(config: {name}Config): {name} {{
        return new {name}(config);
    }}
    
    static createDefault(): {name} {{
        return new {name}();
    }}
}}
"""
            }
        }
        
        self.logger.info("Architectural generator initialized")
    
    def generate_project_structure(
        self,
        patterns: List[str],
        project_name: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Gera estrutura de projeto
        
        Args:
            patterns: Padrões a implementar
            project_name: Nome do projeto
            language: Linguagem de programação
        
        Returns:
            Estrutura de projeto gerada
        """
        self.logger.info(f"Generating project structure for {project_name}")
        
        # Gera prompt para LLM
        prompt = f"""
Generate a project structure for a {language} project named {project_name} that implements the following patterns: {', '.join(patterns)}.

The structure should include:
- Directory organization
- Main entry points
- Configuration files
- Test directories

Return the structure as a tree format.
"""
        
        # Usa LLM para gerar estrutura
        structure_text = self.llm.generate(prompt, max_length=512)
        
        # Parseia estrutura (simplificado)
        structure = self._parse_structure(structure_text, patterns)
        
        return {
            "project_name": project_name,
            "language": language,
            "patterns": patterns,
            "structure": structure,
            "structure_text": structure_text
        }
    
    def generate_module(
        self,
        module_type: str,
        context: str,
        language: str = "python",
        template_data: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Gera módulo base
        
        Args:
            module_type: Tipo de módulo (repository, factory, etc.)
            context: Contexto (ex: 'user', 'product')
            language: Linguagem de programação
            template_data: Dados adicionais para template
        
        Returns:
            Código do módulo gerado
        """
        self.logger.info(f"Generating {module_type} module for {context}")
        
        # Usa template se disponível
        if module_type in self.templates and language in self.templates[module_type]:
            template = self.templates[module_type][language]
            data = template_data or {}
            data["name"] = context.capitalize()
            data["table"] = context.lower() + "s"
            
            code = template.format(**data)
            return code
        
        # Caso contrário, usa LLM
        prompt = f"""
Generate a {module_type} implementation in {language} for {context}.

The code should:
- Follow best practices
- Include proper documentation
- Be production-ready
"""
        
        code = self.llm.generate(prompt, max_length=512)
        return code
    
    def generate_configuration(
        self,
        config_type: str,
        project_type: str = "web"
    ) -> str:
        """
        Gera arquivo de configuração
        
        Args:
            config_type: Tipo de configuração (database, api, etc.)
            project_type: Tipo de projeto
        
        Returns:
            Conteúdo do arquivo de configuração
        """
        self.logger.info(f"Generating {config_type} configuration")
        
        prompt = f"""
Generate a {config_type} configuration file for a {project_type} project.

Include:
- Common settings
- Environment variables
- Best practices
"""
        
        config = self.llm.generate(prompt, max_length=256)
        return config
    
    def generate_from_architecture(
        self,
        architecture_suggestion: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gera código completo baseado em sugestão arquitetural
        
        Args:
            architecture_suggestion: Sugestão de arquitetura
        
        Returns:
            Código gerado organizado por módulos
        """
        self.logger.info("Generating code from architecture suggestion")
        
        patterns = architecture_suggestion.get("recommended_patterns", [])
        project_path = architecture_suggestion.get("project_path", "project")
        project_name = Path(project_path).name
        
        generated = {
            "project_name": project_name,
            "modules": {},
            "structure": None
        }
        
        # Gera estrutura
        structure = self.generate_project_structure(patterns, project_name)
        generated["structure"] = structure
        
        # Gera módulos para cada padrão
        for pattern in patterns:
            if pattern == "repository":
                module = self.generate_module("repository", "entity")
                generated["modules"]["repository.py"] = module
            
            elif pattern == "factory":
                module = self.generate_module("factory", "entity")
                generated["modules"]["factory.py"] = module
        
        return generated
    
    def _parse_structure(self, structure_text: str, patterns: List[str]) -> Dict[str, Any]:
        """
        Parseia texto de estrutura em dicionário
        
        Args:
            structure_text: Texto da estrutura
            patterns: Padrões implementados
        
        Returns:
            Estrutura parseada
        """
        # Simplificado - em produção, parser mais robusto
        structure = {
            "directories": [],
            "files": [],
            "patterns": patterns
        }
        
        lines = structure_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and ('/' in line or '\\' in line):
                if line.endswith('/'):
                    structure["directories"].append(line.rstrip('/'))
                else:
                    structure["files"].append(line)
        
        return structure

