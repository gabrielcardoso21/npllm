"""
Chunking semântico de código
Divide código por função/classe usando AST
"""

import ast
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.utils.logging import get_logger


class CodeChunker:
    """
    Chunker semântico de código
    Divide por função/classe para preservar contexto
    """
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Inicializa chunker
        
        Args:
            chunk_size: Tamanho máximo do chunk (em tokens aproximados)
            chunk_overlap: Overlap entre chunks
        """
        self.logger = get_logger(self.__class__.__name__)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_python(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Chunk código Python por função/classe
        
        Args:
            code: Código Python
            file_path: Caminho do arquivo
        
        Returns:
            Lista de chunks com metadados
        """
        chunks = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    # Extrai função/classe
                    chunk_code = ast.get_source_segment(code, node)
                    if chunk_code is None:
                        continue
                    
                    # Extrai imports e docstring
                    imports = self._extract_imports(code)
                    docstring = ast.get_docstring(node)
                    
                    # Cria chunk
                    chunk = {
                        "code": chunk_code,
                        "context": {
                            "imports": imports,
                            "docstring": docstring
                        },
                        "metadata": {
                            "file": file_path,
                            "name": node.name,
                            "type": "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class",
                            "line_start": node.lineno,
                            "line_end": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
                        }
                    }
                    
                    chunks.append(chunk)
            
            # Se não encontrou funções/classes, cria chunk do arquivo inteiro
            if not chunks:
                chunks.append({
                    "code": code,
                    "context": {
                        "imports": self._extract_imports(code),
                        "docstring": None
                    },
                    "metadata": {
                        "file": file_path,
                        "name": "file",
                        "type": "file",
                        "line_start": 1,
                        "line_end": len(code.split('\n'))
                    }
                })
        
        except SyntaxError as e:
            self.logger.warning(f"Syntax error in {file_path}: {e}. Creating single chunk.")
            chunks.append({
                "code": code,
                "context": {"imports": [], "docstring": None},
                "metadata": {
                    "file": file_path,
                    "name": "file",
                    "type": "file",
                    "error": str(e)
                }
            })
        
        return chunks
    
    def chunk_javascript(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Chunk código JavaScript por função/classe (simplificado)
        
        Args:
            code: Código JavaScript
            file_path: Caminho do arquivo
        
        Returns:
            Lista de chunks
        """
        chunks = []
        
        # Regex para funções e classes
        function_pattern = r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>|class\s+(\w+))'
        
        matches = list(re.finditer(function_pattern, code))
        
        if matches:
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(code)
                
                chunk_code = code[start:end].strip()
                name = match.group(1) or match.group(2) or match.group(3) or "anonymous"
                
                chunks.append({
                    "code": chunk_code,
                    "context": {"imports": self._extract_js_imports(code)},
                    "metadata": {
                        "file": file_path,
                        "name": name,
                        "type": "function" if "function" in match.group(0) or "=>" in match.group(0) else "class",
                        "line_start": code[:start].count('\n') + 1,
                        "line_end": code[:end].count('\n') + 1
                    }
                })
        else:
            # Chunk único
            chunks.append({
                "code": code,
                "context": {"imports": self._extract_js_imports(code)},
                "metadata": {
                    "file": file_path,
                    "name": "file",
                    "type": "file"
                }
            })
        
        return chunks
    
    def chunk_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Chunk arquivo baseado na extensão
        
        Args:
            file_path: Caminho do arquivo
        
        Returns:
            Lista de chunks
        """
        path = Path(file_path)
        
        if not path.exists():
            self.logger.warning(f"File not found: {file_path}")
            return []
        
        code = path.read_text(encoding='utf-8', errors='ignore')
        
        if path.suffix == '.py':
            return self.chunk_python(code, str(file_path))
        elif path.suffix in ['.js', '.jsx', '.ts', '.tsx']:
            return self.chunk_javascript(code, str(file_path))
        else:
            # Chunk genérico (por linhas)
            return self._chunk_generic(code, str(file_path))
    
    def _chunk_generic(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        """Chunk genérico por linhas"""
        lines = code.split('\n')
        chunks = []
        
        current_chunk = []
        current_size = 0
        
        for i, line in enumerate(lines):
            current_chunk.append(line)
            current_size += len(line.split())
            
            if current_size >= self.chunk_size:
                chunks.append({
                    "code": '\n'.join(current_chunk),
                    "context": {},
                    "metadata": {
                        "file": file_path,
                        "name": f"chunk_{len(chunks)}",
                        "type": "generic",
                        "line_start": i - len(current_chunk) + 1,
                        "line_end": i + 1
                    }
                })
                current_chunk = []
                current_size = 0
        
        # Último chunk
        if current_chunk:
            chunks.append({
                "code": '\n'.join(current_chunk),
                "context": {},
                "metadata": {
                    "file": file_path,
                    "name": f"chunk_{len(chunks)}",
                    "type": "generic",
                    "line_start": len(lines) - len(current_chunk) + 1,
                    "line_end": len(lines)
                }
            })
        
        return chunks
    
    def _extract_imports(self, code: str) -> List[str]:
        """Extrai imports de código Python"""
        imports = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(ast.get_source_segment(code, node))
        except:
            pass
        return imports
    
    def _extract_js_imports(self, code: str) -> List[str]:
        """Extrai imports de código JavaScript"""
        imports = []
        import_pattern = r'(?:import|require)\(?[^)]*\)?'
        matches = re.findall(import_pattern, code)
        imports.extend(matches)
        return imports

