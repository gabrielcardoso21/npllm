"""
Content Collector
Collects content from various sources (URL, files, directories, text)
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from src.utils.logging import get_logger


class ContentCollector:
    """
    Coletor de conteúdo
    Coleta conteúdo de diferentes fontes
    """
    
    def __init__(self):
        """Inicializa coletor de conteúdo"""
        self.logger = get_logger(self.__class__.__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.logger.info("Content collector initialized")
    
    def collect_from_url(
        self,
        url: str,
        max_depth: int = 2,
        max_pages: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Coleta conteúdo de uma URL (web scraping)
        
        Args:
            url: URL inicial
            max_depth: Profundidade máxima de navegação
            max_pages: Número máximo de páginas
        
        Returns:
            Lista de documentos coletados
        """
        self.logger.info(f"Collecting content from URL: {url}")
        
        collected = []
        visited = set()
        to_visit = [(url, 0)]  # (url, depth)
        
        while to_visit and len(collected) < max_pages:
            current_url, depth = to_visit.pop(0)
            
            if current_url in visited or depth > max_depth:
                continue
            
            visited.add(current_url)
            
            try:
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove scripts, styles, etc.
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Extrai título
                title = soup.find('title')
                title_text = title.get_text().strip() if title else current_url
                
                # Converte para markdown
                content = md(str(soup), heading_style="ATX")
                
                # Limpa conteúdo
                content = self._clean_content(content)
                
                collected.append({
                    "title": title_text,
                    "content": content,
                    "url": current_url,
                    "type": "web_page"
                })
                
                self.logger.debug(f"Collected: {title_text} ({current_url})")
                
                # Encontra links relacionados (apenas se depth < max_depth)
                if depth < max_depth:
                    base_url = f"{urlparse(current_url).scheme}://{urlparse(current_url).netloc}"
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        absolute_url = urljoin(base_url, href)
                        
                        # Filtra apenas URLs do mesmo domínio
                        if urlparse(absolute_url).netloc == urlparse(url).netloc:
                            if absolute_url not in visited:
                                to_visit.append((absolute_url, depth + 1))
            
            except Exception as e:
                self.logger.warning(f"Error collecting from {current_url}: {e}")
                continue
        
        self.logger.info(f"Collected {len(collected)} pages from {url}")
        return collected
    
    def collect_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Coleta conteúdo de um arquivo local
        
        Args:
            file_path: Caminho do arquivo
        
        Returns:
            Lista com um documento
        """
        self.logger.info(f"Collecting content from file: {file_path}")
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Lê arquivo
        try:
            if path.suffix.lower() == '.md':
                content = path.read_text(encoding='utf-8')
            elif path.suffix.lower() in ['.txt', '.py', '.js', '.html']:
                content = path.read_text(encoding='utf-8')
            else:
                # Tenta ler como texto
                content = path.read_text(encoding='utf-8', errors='ignore')
            
            # Limpa conteúdo
            content = self._clean_content(content)
            
            return [{
                "title": path.stem,
                "content": content,
                "file_path": str(path),
                "type": "file"
            }]
        
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    def collect_from_directory(
        self,
        dir_path: str,
        extensions: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Coleta conteúdo de um diretório
        
        Args:
            dir_path: Caminho do diretório
            extensions: Extensões de arquivo a incluir (ex: ['.py', '.md'])
        
        Returns:
            Lista de documentos coletados
        """
        self.logger.info(f"Collecting content from directory: {dir_path}")
        
        if extensions is None:
            extensions = ['.py', '.md', '.txt', '.js', '.html', '.yaml', '.yml']
        
        path = Path(dir_path)
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Directory not found: {dir_path}")
        
        collected = []
        
        for file_path in path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                try:
                    # Ignora arquivos muito grandes (> 1MB)
                    if file_path.stat().st_size > 1024 * 1024:
                        continue
                    
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    content = self._clean_content(content)
                    
                    # Caminho relativo
                    rel_path = file_path.relative_to(path)
                    
                    collected.append({
                        "title": str(rel_path),
                        "content": content,
                        "file_path": str(file_path),
                        "type": "file"
                    })
                
                except Exception as e:
                    self.logger.warning(f"Error reading {file_path}: {e}")
                    continue
        
        self.logger.info(f"Collected {len(collected)} files from {dir_path}")
        return collected
    
    def collect_from_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Coleta conteúdo de texto direto
        
        Args:
            text: Texto a coletar
            metadata: Metadados adicionais
        
        Returns:
            Lista com um documento
        """
        self.logger.info("Collecting content from text")
        
        content = self._clean_content(text)
        title = metadata.get("title", "Text Input") if metadata else "Text Input"
        
        return [{
            "title": title,
            "content": content,
            "type": "text",
            "metadata": metadata
        }]
    
    def _clean_content(self, content: str) -> str:
        """
        Limpa conteúdo removendo caracteres desnecessários
        
        Args:
            content: Conteúdo bruto
        
        Returns:
            Conteúdo limpo
        """
        # Remove múltiplas linhas em branco
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Remove espaços em excesso
        content = re.sub(r'[ \t]+', ' ', content)
        
        # Remove caracteres de controle
        content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)
        
        return content.strip()

