"""
Course Learner
Learns patterns and knowledge from course content
"""

import json
import re
from typing import List, Dict, Any, Optional

from src.utils.logging import get_logger


class CourseLearner:
    """
    Sistema de aprendizado de curso
    Aprende padrões e conhecimento do curso
    """
    
    def __init__(self, base_model, storage):
        """
        Inicializa sistema de aprendizado de curso
        
        Args:
            base_model: Instância do LLM Base
            storage: Instância de PostgreSQLStorage
        """
        self.logger = get_logger(self.__class__.__name__)
        self.base_model = base_model
        self.storage = storage
        self.logger.info("Course learner initialized")
    
    def learn_from_course(self, course_id: int) -> Dict[str, Any]:
        """
        Aprende padrões e conceitos de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Resumo do aprendizado
        """
        self.logger.info(f"Learning from course {course_id}")
        
        # Carrega conteúdo do curso
        content_chunks = self.storage.get_course_content(course_id)
        
        if not content_chunks:
            self.logger.warning(f"No content found for course {course_id}")
            return {
                "status": "error",
                "message": "No content to learn from"
            }
        
        self.logger.info(f"Processing {len(content_chunks)} content chunks")
        
        # Extrai padrões e conceitos
        all_patterns = []
        all_concepts = []
        
        # Processa em lotes para eficiência
        batch_size = 10
        for i in range(0, len(content_chunks), batch_size):
            batch = content_chunks[i:i + batch_size]
            
            for chunk in batch:
                # Extrai padrões do chunk
                patterns = self.extract_patterns(chunk['content'])
                all_patterns.extend(patterns)
                
                # Extrai conceitos do chunk
                concepts = self.extract_concepts(chunk['content'])
                all_concepts.extend(concepts)
        
        # Consolida conhecimento
        consolidated = self.consolidate_knowledge(all_patterns, all_concepts)
        
        # Armazena conceitos aprendidos
        concepts_stored = 0
        for concept in consolidated['concepts']:
            self.storage.store_learned_concept(
                course_id=course_id,
                concept_name=concept['name'],
                description=concept['description'],
                examples=concept.get('examples', []),
                patterns=concept.get('patterns', []),
                confidence=concept.get('confidence', 0.5)
            )
            concepts_stored += 1
        
        self.logger.info(f"Stored {concepts_stored} learned concepts")
        
        return {
            "status": "success",
            "course_id": course_id,
            "chunks_processed": len(content_chunks),
            "patterns_found": len(all_patterns),
            "concepts_learned": concepts_stored,
            "concepts": consolidated['concepts']
        }
    
    def extract_patterns(self, content: str) -> List[Dict[str, Any]]:
        """
        Extrai padrões arquiteturais do conteúdo
        
        Args:
            content: Conteúdo a analisar
        
        Returns:
            Lista de padrões encontrados
        """
        patterns = []
        
        # Usa LLM Base para identificar padrões
        prompt = f"""Analyze the following content and identify architectural patterns, design patterns, or coding patterns.
        
Content:
{content[:1000]}

Return a JSON list of patterns found, each with:
- name: pattern name
- description: brief description
- example: code example if available

Format: JSON array only, no markdown."""
        
        try:
            response = self.base_model.generate(prompt, max_length=512)
            
            # Tenta extrair JSON da resposta
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                patterns_data = json.loads(json_match.group())
                patterns = patterns_data if isinstance(patterns_data, list) else []
        except Exception as e:
            self.logger.warning(f"Error extracting patterns: {e}")
            # Fallback: extração simples por regex
            patterns = self._extract_patterns_simple(content)
        
        return patterns
    
    def extract_concepts(self, content: str) -> List[Dict[str, Any]]:
        """
        Extrai conceitos principais do conteúdo
        
        Args:
            content: Conteúdo a analisar
        
        Returns:
            Lista de conceitos encontrados
        """
        concepts = []
        
        # Usa LLM Base para identificar conceitos
        prompt = f"""Analyze the following content and identify key concepts, topics, or important ideas.
        
Content:
{content[:1000]}

Return a JSON list of concepts, each with:
- name: concept name
- description: brief description
- examples: list of examples (if any)

Format: JSON array only, no markdown."""
        
        try:
            response = self.base_model.generate(prompt, max_length=512)
            
            # Tenta extrair JSON da resposta
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                concepts_data = json.loads(json_match.group())
                concepts = concepts_data if isinstance(concepts_data, list) else []
        except Exception as e:
            self.logger.warning(f"Error extracting concepts: {e}")
            # Fallback: extração simples
            concepts = self._extract_concepts_simple(content)
        
        return concepts
    
    def consolidate_knowledge(
        self,
        patterns: List[Dict[str, Any]],
        concepts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Consolida conhecimento de padrões e conceitos
        
        Args:
            patterns: Lista de padrões
            concepts: Lista de conceitos
        
        Returns:
            Conhecimento consolidado
        """
        # Agrupa padrões similares
        unique_patterns = {}
        for pattern in patterns:
            name = pattern.get('name', 'Unknown')
            if name not in unique_patterns:
                unique_patterns[name] = pattern
            else:
                # Merge com padrão existente
                existing = unique_patterns[name]
                if 'examples' not in existing:
                    existing['examples'] = []
                if 'examples' in pattern:
                    existing['examples'].extend(pattern['examples'])
        
        # Agrupa conceitos similares
        unique_concepts = {}
        for concept in concepts:
            name = concept.get('name', 'Unknown')
            if name not in unique_concepts:
                unique_concepts[name] = concept
            else:
                # Merge com conceito existente
                existing = unique_concepts[name]
                if 'examples' not in existing:
                    existing['examples'] = []
                if 'examples' in concept:
                    existing['examples'].extend(concept['examples'])
        
        # Calcula confiança baseada em frequência
        consolidated_concepts = []
        for name, concept in unique_concepts.items():
            # Conta quantas vezes apareceu
            frequency = sum(1 for c in concepts if c.get('name') == name)
            confidence = min(0.5 + (frequency * 0.1), 1.0)
            
            consolidated_concepts.append({
                'name': name,
                'description': concept.get('description', ''),
                'examples': concept.get('examples', [])[:5],  # Limita a 5 exemplos
                'patterns': [p for p in unique_patterns.values() if name.lower() in p.get('name', '').lower()],
                'confidence': confidence
            })
        
        return {
            'patterns': list(unique_patterns.values()),
            'concepts': consolidated_concepts,
            'total_patterns': len(unique_patterns),
            'total_concepts': len(consolidated_concepts)
        }
    
    def get_learned_concepts(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Obtém conceitos aprendidos de um curso
        
        Args:
            course_id: ID do curso
        
        Returns:
            Lista de conceitos aprendidos
        """
        return self.storage.get_learned_concepts(course_id)
    
    def _extract_patterns_simple(self, content: str) -> List[Dict[str, Any]]:
        """Extração simples de padrões por regex (fallback)"""
        patterns = []
        
        # Detecta padrões comuns
        if re.search(r'class\s+\w+.*:\s*$', content, re.MULTILINE):
            patterns.append({
                'name': 'Class Definition',
                'description': 'Object-oriented class structure'
            })
        
        if re.search(r'def\s+\w+\(.*\):', content):
            patterns.append({
                'name': 'Function Definition',
                'description': 'Function or method definition'
            })
        
        return patterns
    
    def _extract_concepts_simple(self, content: str) -> List[Dict[str, Any]]:
        """Extração simples de conceitos por regex (fallback)"""
        concepts = []
        
        # Extrai títulos/headers (markdown)
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        for header in headers[:5]:  # Limita a 5
            concepts.append({
                'name': header.strip(),
                'description': f'Topic: {header.strip()}'
            })
        
        return concepts

