"""
REST API Server
FastAPI server for npllm system communication
"""

"""
REST API Server
FastAPI server for npllm system communication
"""

import sys
import os

# Adicionar raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import json

from src.main import initialize_system, NpllmSystem
from src.utils.logging import get_logger

app = FastAPI(
    title="npllm API",
    description="API para comunicação com o sistema npllm",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sistema global (inicializado no startup)
system: Optional[NpllmSystem] = None
logger = get_logger("npllm_api")


@app.on_event("startup")
async def startup_event():
    """Inicializa sistema no startup"""
    global system
    logger.info("Initializing npllm system...")
    try:
        system = initialize_system()
        logger.info("npllm system initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Fecha sistema no shutdown"""
    global system
    if system:
        logger.info("Closing npllm system...")
        system.close()
        logger.info("System closed")


# Models
class QueryRequest(BaseModel):
    query: str
    project_path: Optional[str] = None
    file_path: Optional[str] = None
    course_context: Optional[int] = None


class QueryResponse(BaseModel):
    response: str
    adapter_used: str
    course_context_used: bool


class FeedbackRequest(BaseModel):
    query: str
    response: str
    user_reaction: str
    user_action: Optional[str] = None  # "accept", "edit", "delete", "ignore"
    explicit_feedback: Optional[float] = None


class CourseCreateRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    source_type: str  # "url", "file", "directory", "text"
    source_path: str


class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    source_type: str
    source_path: str
    status: str
    created_at: str


class CourseStatusResponse(BaseModel):
    id: int
    name: str
    status: str
    content_chunks: int
    concepts_learned: int
    created_at: str
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class ValidationRequest(BaseModel):
    automatic: bool = False
    num_questions: int = 10
    validation_threshold: float = 0.75


# Endpoints

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "npllm",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check detalhado"""
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    status = system.get_system_status()
    return status


@app.post("/query")
async def process_query(request: QueryRequest, stream: bool = False):
    """
    Processa uma query do usuário
    
    Args:
        request: Query request com query, project_path, file_path, course_context
        stream: Se True, retorna streaming SSE (Server-Sent Events)
    
    Returns:
        Resposta do sistema (JSON ou SSE stream)
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        if stream:
            # Modo "fake streaming" - envia status de progresso
            async def generate_progress():
                # Status: Iniciando
                yield f"data: {json.dumps({'type': 'status', 'stage': 'starting', 'message': 'Iniciando processamento...'})}\n\n"
                
                # Processa query
                query_text = request.query
                
                # Status: Preparando contexto
                if request.course_context:
                    yield f"data: {json.dumps({'type': 'status', 'stage': 'context', 'message': 'Buscando contexto do curso...'})}\n\n"
                    try:
                        from src.learning.content_processor import ContentProcessor
                        processor = ContentProcessor()
                        query_embedding = processor.generate_embedding(query_text)
                        relevant_chunks = system.storage.search_course_content(
                            request.course_context,
                            query_embedding,
                            top_k=3
                        )
                        if relevant_chunks:
                            context = "\n\nRelevant context:\n"
                            for chunk in relevant_chunks:
                                context += f"- {chunk['title']}: {chunk['content'][:200]}...\n"
                            query_text = f"{context}\n\nUser query: {query_text}"
                            yield f"data: {json.dumps({'type': 'status', 'stage': 'context', 'message': f'Contexto encontrado: {len(relevant_chunks)} chunks relevantes'})}\n\n"
                    except Exception as e:
                        logger.warning(f"Error retrieving course context: {e}")
                        yield f"data: {json.dumps({'type': 'status', 'stage': 'context', 'message': 'Contexto não disponível, continuando...'})}\n\n"
                
                # Status: Selecionando adapter
                yield f"data: {json.dumps({'type': 'status', 'stage': 'adapter_selection', 'message': 'Selecionando adapter apropriado...'})}\n\n"
                adapter_name = system.selector.select(
                    file_path=request.file_path,
                    project_structure={"path": request.project_path} if request.project_path else None
                )
                yield f"data: {json.dumps({'type': 'status', 'stage': 'adapter_selected', 'message': f'Adapter selecionado: {adapter_name}'})}\n\n"
                
                # Status: Carregando adapter
                adapter_loaded = False
                if adapter_name and adapter_name != "default":
                    yield f"data: {json.dumps({'type': 'status', 'stage': 'adapter_loading', 'message': f'Carregando adapter {adapter_name}...'})}\n\n"
                    try:
                        adapter_loaded = system.adapter_manager.load_adapter_for_generation(
                            adapter_name, 
                            system.base_model
                        )
                        if adapter_loaded:
                            yield f"data: {json.dumps({'type': 'status', 'stage': 'adapter_loaded', 'message': f'Adapter {adapter_name} carregado com sucesso'})}\n\n"
                        else:
                            yield f"data: {json.dumps({'type': 'status', 'stage': 'adapter_fallback', 'message': f'Adapter não encontrado, usando modelo base'})}\n\n"
                    except Exception as e:
                        logger.warning(f"Could not load adapter {adapter_name}: {e}")
                        yield f"data: {json.dumps({'type': 'status', 'stage': 'adapter_error', 'message': f'Erro ao carregar adapter: {str(e)[:50]}'})}\n\n"
                
                # Status: Carregando modelo (se necessário)
                if system.base_model._model is None:
                    yield f"data: {json.dumps({'type': 'status', 'stage': 'model_loading', 'message': 'Carregando modelo base...'})}\n\n"
                
                # Status: Gerando resposta
                yield f"data: {json.dumps({'type': 'status', 'stage': 'generating', 'message': 'Gerando resposta...'})}\n\n"
                
                # Gera resposta completa (sem streaming real)
                response = system.base_model.generate(query_text, max_length=512, stream=False)
                
                # Status: Processando resposta
                yield f"data: {json.dumps({'type': 'status', 'stage': 'processing', 'message': 'Processando resposta...'})}\n\n"
                
                # Armazena adapter para feedback
                system._last_adapter_name = adapter_name
                
                # Status: Finalizando
                yield f"data: {json.dumps({'type': 'status', 'stage': 'finalizing', 'message': 'Finalizando...'})}\n\n"
                
                # Resposta completa
                yield f"data: {json.dumps({'type': 'done', 'response': response, 'adapter_used': adapter_name, 'adapter_applied': adapter_loaded, 'message': 'Resposta gerada com sucesso'})}\n\n"
            
            return StreamingResponse(
                generate_progress(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"
                }
            )
        else:
            # Modo normal (não-streaming)
            result = system.process_query(
                query=request.query,
                project_path=request.project_path,
                file_path=request.file_path,
                course_context=request.course_context
            )
            
            return QueryResponse(
                response=result["response"],
                adapter_used=result["adapter_used"],
                course_context_used=result.get("course_context_used", False)
            )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def capture_feedback(request: FeedbackRequest):
    """
    Captura feedback do usuário
    
    Args:
        request: Feedback request
    
    Returns:
        Status da operação
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        from src.feedback.implicit import UserAction
        
        user_action = None
        if request.user_action:
            action_map = {
                "accept": UserAction.ACCEPT,
                "edit": UserAction.EDIT,
                "delete": UserAction.DELETE,
                "ignore": UserAction.IGNORE
            }
            user_action = action_map.get(request.user_action)
        
        system.capture_feedback(
            query=request.query,
            response=request.response,
            user_reaction=request.user_reaction,
            user_action=user_action,
            explicit_feedback=request.explicit_feedback
        )
        
        return {"status": "success", "message": "Feedback captured"}
    
    except Exception as e:
        logger.error(f"Error capturing feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/courses", response_model=CourseResponse)
async def create_course(request: CourseCreateRequest):
    """
    Cria um novo curso
    
    Args:
        request: Course creation request
    
    Returns:
        Curso criado
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        course = system.create_course(
            name=request.name,
            description=request.description,
            source_type=request.source_type,
            source_path=request.source_path
        )
        
        return CourseResponse(**course)
    
    except Exception as e:
        logger.error(f"Error creating course: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/courses", response_model=List[CourseResponse])
async def list_courses():
    """
    Lista todos os cursos
    
    Returns:
        Lista de cursos
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        courses = system.list_courses()
        return [CourseResponse(**course) for course in courses]
    
    except Exception as e:
        logger.error(f"Error listing courses: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/courses/{course_id}", response_model=CourseStatusResponse)
async def get_course_status(course_id: int):
    """
    Obtém status de um curso
    
    Args:
        course_id: ID do curso
    
    Returns:
        Status do curso
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        status = system.get_course_status(course_id)
        return CourseStatusResponse(**status)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting course status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/courses/{course_id}/start")
async def start_course_learning(course_id: int):
    """
    Inicia aprendizado de um curso
    
    Args:
        course_id: ID do curso
    
    Returns:
        Resultado do aprendizado
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        result = system.start_course_learning(course_id)
        return result
    
    except Exception as e:
        logger.error(f"Error starting course learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/courses/{course_id}/concepts")
async def get_course_concepts(course_id: int):
    """
    Obtém conceitos aprendidos de um curso
    
    Args:
        course_id: ID do curso
    
    Returns:
        Lista de conceitos aprendidos
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        concepts = system.get_course_concepts(course_id)
        return {"course_id": course_id, "concepts": concepts}
    
    except Exception as e:
        logger.error(f"Error getting course concepts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/courses/{course_id}/validate")
async def validate_course(course_id: int, request: Optional[ValidationRequest] = None):
    """
    Valida um curso (manual ou automático)
    
    Args:
        course_id: ID do curso
        request: Parâmetros de validação (opcional, enviar no body)
    
    Returns:
        Resultado da validação
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        # Se request não foi enviado, usar valores padrão
        if request is None:
            request = ValidationRequest()
        
        if request.automatic:
            result = system.validate_course(
                course_id,
                automatic=True,
                num_questions=request.num_questions,
                validation_threshold=request.validation_threshold
            )
        else:
            result = system.validate_course(course_id, automatic=False)
        
        return result
    
    except Exception as e:
        logger.error(f"Error validating course: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sleep")
async def trigger_sleep(force: bool = False):
    """
    Aciona consolidação (sono) manualmente
    
    Args:
        force: Se True, força consolidação mesmo se sistema estiver ativo
    
    Returns:
        Resultado da consolidação
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        result = system.trigger_sleep(force=force)
        # Garantir que retorna dict
        if result is None:
            result = {"status": "completed", "message": "Sleep consolidation completed"}
        elif not isinstance(result, dict):
            result = {"status": "completed", "result": str(result)}
        return result
    
    except Exception as e:
        logger.error(f"Error triggering sleep: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
async def get_status():
    """
    Obtém status completo do sistema
    
    Returns:
        Status do sistema
    """
    if not system:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        return system.get_system_status()
    
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Inicia servidor API
    
    Args:
        host: Host para bind
        port: Porta para bind
    """
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()

