"""
Course Validator
Automatically validates if the system learned from a course
Uses LLM as judge and semantic similarity
"""

import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

from src.utils.logging import get_logger


class CourseValidator:
    """
    Validador automático de cursos
    Gera perguntas focadas e valida respostas automaticamente
    """
    
    def __init__(self, base_model, storage, content_processor):
        """
        Inicializa validador de curso
        
        Args:
            base_model: Instância do LLM Base
            storage: Instância de PostgreSQLStorage
            content_processor: Instância de ContentProcessor
        """
        self.logger = get_logger(self.__class__.__name__)
        self.base_model = base_model
        self.storage = storage
        self.content_processor = content_processor
        self.embedding_model = content_processor.embedding_model
        self.logger.info("Course validator initialized")
    
    def validate_course(
        self,
        course_id: int,
        num_questions: int = 10,
        validation_threshold: float = 0.75
    ) -> Dict[str, Any]:
        """
        Valida automaticamente se o sistema aprendeu do curso
        
        Args:
            course_id: ID do curso
            num_questions: Número de perguntas para gerar
            validation_threshold: Threshold mínimo para validação (0.0 a 1.0)
        
        Returns:
            Resultado da validação com score e detalhes
        """
        self.logger.info(f"Validating course {course_id} with {num_questions} questions")
        
        # 1. Gera perguntas focadas baseadas no conteúdo
        questions = self.generate_validation_questions(course_id, num_questions)
        
        if not questions:
            return {
                "status": "error",
                "message": "Could not generate validation questions"
            }
        
        # 2. Responde cada pergunta usando conhecimento do curso
        validation_results = []
        total_score = 0.0
        
        for question_data in questions:
            question = question_data['question']
            expected_content = question_data['content']
            
            # Responde usando conhecimento do curso
            response = self._answer_with_course_context(question, course_id)
            
            # Valida resposta
            validation_score = self._validate_answer(
                question=question,
                answer=response,
                expected_content=expected_content
            )
            
            validation_results.append({
                "question": question,
                "answer": response,
                "score": validation_score,
                "expected_content": expected_content[:200] + "..." if len(expected_content) > 200 else expected_content
            })
            
            total_score += validation_score
        
        # Score médio
        average_score = total_score / len(validation_results)
        
        # Determina se passou
        passed = average_score >= validation_threshold
        
        result = {
            "status": "passed" if passed else "failed",
            "course_id": course_id,
            "average_score": average_score,
            "validation_threshold": validation_threshold,
            "num_questions": len(questions),
            "passed": passed,
            "results": validation_results
        }
        
        self.logger.info(
            f"Course {course_id} validation: {'PASSED' if passed else 'FAILED'} "
            f"(score: {average_score:.2f}, threshold: {validation_threshold})"
        )
        
        return result
    
    def generate_validation_questions(
        self,
        course_id: int,
        num_questions: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Gera perguntas focadas baseadas no conteúdo do curso
        
        Args:
            course_id: ID do curso
            num_questions: Número de perguntas
        
        Returns:
            Lista de perguntas com conteúdo esperado
        """
        self.logger.info(f"Generating {num_questions} validation questions for course {course_id}")
        
        # Obtém conteúdo do curso
        content_chunks = self.storage.get_course_content(course_id)
        
        if not content_chunks:
            self.logger.warning(f"No content found for course {course_id}")
            return []
        
        # Seleciona chunks representativos (diversos)
        selected_chunks = self._select_representative_chunks(content_chunks, num_questions)
        
        # Gera perguntas para cada chunk
        questions = []
        for chunk in selected_chunks:
            question = self._generate_question_from_chunk(chunk['content'])
            
            if question:
                questions.append({
                    "question": question,
                    "content": chunk['content'],
                    "chunk_id": chunk['id']
                })
        
        self.logger.info(f"Generated {len(questions)} validation questions")
        return questions
    
    def _select_representative_chunks(
        self,
        chunks: List[Dict[str, Any]],
        num_chunks: int
    ) -> List[Dict[str, Any]]:
        """
        Seleciona chunks representativos (diversos)
        
        Args:
            chunks: Lista de chunks
            num_chunks: Número de chunks a selecionar
        
        Returns:
            Lista de chunks selecionados
        """
        if len(chunks) <= num_chunks:
            return chunks
        
        # Seleciona chunks distribuídos uniformemente
        step = len(chunks) // num_chunks
        selected = []
        
        for i in range(0, len(chunks), step):
            if len(selected) < num_chunks:
                selected.append(chunks[i])
        
        # Preenche com últimos se necessário
        while len(selected) < num_chunks and len(selected) < len(chunks):
            selected.append(chunks[len(selected)])
        
        return selected[:num_chunks]
    
    def _generate_question_from_chunk(self, content: str) -> Optional[str]:
        """
        Gera uma pergunta focada a partir de um chunk de conteúdo
        
        Args:
            content: Conteúdo do chunk
        
        Returns:
            Pergunta gerada ou None
        """
        prompt = f"""Based on the following content, generate a focused question that tests understanding of the key concepts.

Content:
{content[:800]}

Generate a single, specific question that can be answered based on this content. The question should test comprehension, not just recall.

Question:"""
        
        try:
            response = self.base_model.generate(prompt, max_length=256)
            
            # Limpa resposta (remove prefixos comuns)
            question = response.strip()
            if question.startswith("Question:"):
                question = question[9:].strip()
            if question.startswith("Q:"):
                question = question[2:].strip()
            
            # Remove pontuação final se não for interrogação
            if question and not question.endswith("?"):
                question = question.rstrip(".") + "?"
            
            return question if question else None
        
        except Exception as e:
            self.logger.warning(f"Error generating question: {e}")
            return None
    
    def _answer_with_course_context(
        self,
        question: str,
        course_id: int
    ) -> str:
        """
        Responde pergunta usando conhecimento do curso
        
        Args:
            question: Pergunta
            course_id: ID do curso
        
        Returns:
            Resposta gerada
        """
        # Busca conteúdo relevante do curso
        query_embedding = self.content_processor.generate_embedding(question)
        relevant_chunks = self.storage.search_course_content(
            course_id,
            query_embedding,
            top_k=3
        )
        
        # Monta contexto
        context = ""
        if relevant_chunks:
            context = "\n\nRelevant context from course:\n"
            for chunk in relevant_chunks:
                context += f"{chunk['content'][:300]}...\n\n"
        
        # Gera resposta com contexto
        full_prompt = f"{context}\n\nQuestion: {question}\n\nAnswer based on the context above:"
        
        try:
            response = self.base_model.generate(full_prompt, max_length=512)
            return response.strip()
        except Exception as e:
            self.logger.warning(f"Error generating answer: {e}")
            return ""
    
    def _validate_answer(
        self,
        question: str,
        answer: str,
        expected_content: str
    ) -> float:
        """
        Valida resposta usando múltiplas técnicas
        
        Args:
            question: Pergunta original
            answer: Resposta gerada
            expected_content: Conteúdo esperado (chunk original)
        
        Returns:
            Score de validação (0.0 a 1.0)
        """
        # 1. Similaridade semântica (embedding)
        semantic_score = self._semantic_similarity(answer, expected_content)
        
        # 2. LLM como juiz (avaliador)
        llm_judge_score = self._llm_judge_validation(question, answer, expected_content)
        
        # 3. Score combinado (peso: 50% semântico + 50% LLM judge)
        combined_score = 0.5 * semantic_score + 0.5 * llm_judge_score
        
        return combined_score
    
    def _semantic_similarity(
        self,
        answer: str,
        expected_content: str
    ) -> float:
        """
        Calcula similaridade semântica entre resposta e conteúdo esperado
        
        Args:
            answer: Resposta gerada
            expected_content: Conteúdo esperado
        
        Returns:
            Score de similaridade (0.0 a 1.0)
        """
        try:
            # Gera embeddings
            answer_embedding = self.embedding_model.encode(answer, convert_to_numpy=True)
            expected_embedding = self.embedding_model.encode(expected_content, convert_to_numpy=True)
            
            # Calcula similaridade de cosseno
            similarity = np.dot(answer_embedding, expected_embedding) / (
                np.linalg.norm(answer_embedding) * np.linalg.norm(expected_embedding)
            )
            
            # Normaliza para 0.0 a 1.0 (similaridade de cosseno já está em -1 a 1)
            normalized = (similarity + 1) / 2
            
            return float(normalized)
        
        except Exception as e:
            self.logger.warning(f"Error calculating semantic similarity: {e}")
            return 0.5  # Score neutro em caso de erro
    
    def _llm_judge_validation(
        self,
        question: str,
        answer: str,
        expected_content: str
    ) -> float:
        """
        Usa LLM como juiz para validar resposta
        
        Args:
            question: Pergunta original
            answer: Resposta gerada
            expected_content: Conteúdo esperado
        
        Returns:
            Score de validação (0.0 a 1.0)
        """
        prompt = f"""You are an evaluator. Compare the generated answer with the expected content and rate how well the answer demonstrates understanding.

Question: {question}

Generated Answer:
{answer[:500]}

Expected Content (reference):
{expected_content[:500]}

Rate the answer on a scale of 0.0 to 1.0, where:
- 1.0 = Perfect understanding, answer is accurate and complete
- 0.8 = Good understanding, answer is mostly correct
- 0.6 = Partial understanding, answer has some correct elements
- 0.4 = Limited understanding, answer is mostly incorrect
- 0.0 = No understanding, answer is completely wrong

Respond with ONLY a number between 0.0 and 1.0 (e.g., 0.75):"""
        
        try:
            response = self.base_model.generate(prompt, max_length=128)
            
            # Extrai número da resposta
            import re
            numbers = re.findall(r'\d+\.?\d*', response)
            
            if numbers:
                score = float(numbers[0])
                # Garante que está entre 0.0 e 1.0
                score = max(0.0, min(1.0, score))
                return score
            
            return 0.5  # Score neutro se não conseguir extrair
        
        except Exception as e:
            self.logger.warning(f"Error in LLM judge validation: {e}")
            return 0.5  # Score neutro em caso de erro

