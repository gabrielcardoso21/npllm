"""
Cursor Adapter
Adapter para fazer o npllm funcionar como um provider OpenAI-compatible
Permite que o Cursor use o npllm como se fosse OpenAI/Anthropic
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.main import initialize_system
from src.utils.logging import get_logger

logger = get_logger("cursor_adapter")

# Inicializa sistema
system = None

def get_system():
    """Lazy initialization do sistema"""
    global system
    if system is None:
        system = initialize_system()
    return system


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "npllm"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 8192
    stream: Optional[bool] = False


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str = "stop"


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Dict[str, int]


def create_cursor_adapter_app() -> FastAPI:
    """
    Cria app FastAPI que funciona como adapter OpenAI-compatible
    para o Cursor IDE
    """
    app = FastAPI(title="npllm Cursor Adapter")
    
    @app.post("/v1/chat/completions")
    async def chat_completions(request: ChatCompletionRequest):
        """
        Endpoint OpenAI-compatible para chat completions
        Traduz requisições do Cursor para o formato do npllm
        """
        try:
            sys = get_system()
            
            # Extrai última mensagem do usuário
            user_messages = [msg for msg in request.messages if msg.role == "user"]
            if not user_messages:
                raise HTTPException(status_code=400, detail="No user message found")
            
            query = user_messages[-1].content
            
            # Extrai contexto de mensagens anteriores (histórico)
            conversation_history = []
            for msg in request.messages[:-1]:  # Todas exceto a última
                if msg.role in ["user", "assistant"]:
                    conversation_history.append(f"{msg.role}: {msg.content}")
            
            # Se há histórico, adiciona ao contexto
            if conversation_history:
                history_context = "\n\nPrevious conversation:\n" + "\n".join(conversation_history[-6:])  # Últimas 6 mensagens
                query = f"{history_context}\n\nUser: {query}"
            
            # Processa query com npllm
            result = sys.process_query(
                query=query,
                project_path=None,  # Cursor já fornece contexto de código
                file_path=None
            )
            
            response_text = result.get('response', '')
            
            # Formata resposta no formato OpenAI
            import time
            response = ChatCompletionResponse(
                id=f"npllm-{int(time.time())}",
                created=int(time.time()),
                model=request.model,
                choices=[
                    ChatCompletionChoice(
                        index=0,
                        message=ChatMessage(
                            role="assistant",
                            content=response_text
                        ),
                        finish_reason="stop"
                    )
                ],
                usage={
                    "prompt_tokens": len(query.split()),  # Aproximação
                    "completion_tokens": len(response_text.split()),
                    "total_tokens": len(query.split()) + len(response_text.split())
                }
            )
            
            return response.dict()
        
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/health")
    async def health():
        """Health check"""
        return {"status": "healthy", "service": "npllm-cursor-adapter"}
    
    return app


if __name__ == "__main__":
    import uvicorn
    app = create_cursor_adapter_app()
    print("🚀 npllm Cursor Adapter iniciado!")
    print("📡 Endpoint: http://localhost:8001/v1/chat/completions")
    print("💡 Configure o Cursor para usar esta URL")
    print("⚠️  Pressione Ctrl+C para parar\n")
    uvicorn.run(app, host="0.0.0.0", port=8001)

