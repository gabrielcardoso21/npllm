"""
Interface web leve usando Gradio
Conecta-se à API FastAPI existente
"""

import gradio as gr
import requests
import json
from typing import Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# URL da API (pode ser local ou remota)
API_URL = "http://localhost:8000"


def query_api(
    query: str,
    project_path: Optional[str] = None,
    file_path: Optional[str] = None,
    stream: bool = False
) -> tuple[str, Optional[str]]:
    """
    Envia query para a API e retorna resposta
    
    Returns:
        (response_text, error_message)
    """
    try:
        url = f"{API_URL}/query"
        params = {"stream": "true" if stream else "false"}
        
        payload = {
            "query": query,
        }
        
        if project_path:
            payload["project_path"] = project_path
        if file_path:
            payload["file_path"] = file_path
        
        if stream:
            # Para streaming, retorna status updates
            response = requests.post(url, json=payload, params=params, stream=True, timeout=120)
            response.raise_for_status()
            
            full_response = ""
            status_updates = []
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])  # Remove "data: "
                            
                            if data.get('type') == 'status':
                                status = data.get('stage', '')
                                message = data.get('message', '')
                                status_updates.append(f"🔄 {status}: {message}")
                            elif data.get('type') == 'done':
                                full_response = data.get('response', '')
                                break
                        except json.JSONDecodeError:
                            continue
            
            status_text = "\n".join(status_updates) if status_updates else ""
            return full_response, status_text
        else:
            # Modo normal
            response = requests.post(url, json=payload, params=params, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", ""), None
            
    except requests.exceptions.ConnectionError:
        error = "❌ Erro: Não foi possível conectar à API. Verifique se a API está rodando em http://localhost:8000"
        return "", error
    except requests.exceptions.Timeout:
        error = "❌ Erro: Timeout ao aguardar resposta da API"
        return "", error
    except requests.exceptions.HTTPError as e:
        error = f"❌ Erro HTTP: {e.response.status_code} - {e.response.text[:200]}"
        return "", error
    except Exception as e:
        error = f"❌ Erro inesperado: {str(e)}"
        logger.error(f"Error in query_api: {e}", exc_info=True)
        return "", error


def send_feedback(
    query: str,
    response: str,
    feedback_type: str,
    rating: Optional[int] = None
) -> str:
    """
    Envia feedback para a API
    
    Args:
        query: Query original
        response: Resposta gerada
        feedback_type: "positive", "negative", "neutral", "edit", "delete"
        rating: Nota de 1-5 (opcional)
    """
    try:
        url = f"{API_URL}/feedback"
        
        payload = {
            "query": query,
            "response": response,
            "feedback_type": feedback_type,
        }
        
        if rating:
            payload["rating"] = rating
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        return "✅ Feedback enviado com sucesso!"
        
    except Exception as e:
        error = f"❌ Erro ao enviar feedback: {str(e)}"
        logger.error(f"Error in send_feedback: {e}", exc_info=True)
        return error


def check_health() -> str:
    """Verifica saúde da API"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        health = data.get("health", {})
        status = "✅ API Online" if health.get("healthy") else "⚠️ API com problemas"
        
        info = f"{status}\n"
        info += f"Storage: {data.get('storage_status', 'unknown')}\n"
        info += f"Cursos: {data.get('courses_count', 0)}"
        
        return info
    except Exception as e:
        return f"❌ Erro ao verificar saúde: {str(e)}"


def create_interface():
    """Cria interface Gradio"""
    
    with gr.Blocks(
        title="NPLLM - Assistente de Código",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as demo:
        gr.Markdown(
            """
            # 🧠 NPLLM - Assistente de Código Neuroplástico
            
            Assistente de código que aprende padrões arquiteturais e melhora continuamente.
            """
        )
        
        with gr.Row():
            with gr.Column(scale=3):
                query_input = gr.Textbox(
                    label="💬 Sua Pergunta",
                    placeholder="Ex: Crie uma função Python para calcular fibonacci",
                    lines=5,
                    max_lines=10
                )
                
                with gr.Row():
                    project_path_input = gr.Textbox(
                        label="📁 Caminho do Projeto (opcional)",
                        placeholder="/path/to/project",
                        scale=2
                    )
                    file_path_input = gr.Textbox(
                        label="📄 Arquivo (opcional)",
                        placeholder="src/main.py",
                        scale=1
                    )
                
                with gr.Row():
                    submit_btn = gr.Button("🚀 Enviar", variant="primary", scale=1)
                    stream_btn = gr.Button("📡 Enviar com Streaming", variant="secondary", scale=1)
                    health_btn = gr.Button("💚 Verificar API", scale=1)
                
                status_output = gr.Textbox(
                    label="📊 Status",
                    lines=3,
                    interactive=False,
                    visible=False
                )
                
                response_output = gr.Textbox(
                    label="🤖 Resposta",
                    lines=15,
                    max_lines=30,
                    interactive=True
                )
                
            with gr.Column(scale=1):
                gr.Markdown("### 📝 Feedback")
                
                feedback_type = gr.Radio(
                    choices=["positive", "negative", "neutral", "edit", "delete"],
                    label="Tipo de Feedback",
                    value="neutral"
                )
                
                rating = gr.Slider(
                    minimum=1,
                    maximum=5,
                    step=1,
                    label="Nota (1-5)",
                    value=3
                )
                
                feedback_btn = gr.Button("📤 Enviar Feedback", variant="secondary")
                feedback_output = gr.Textbox(
                    label="Resultado",
                    lines=2,
                    interactive=False
                )
                
                gr.Markdown("---")
                gr.Markdown("### ℹ️ Informações")
                health_info = gr.Textbox(
                    label="Status da API",
                    lines=5,
                    interactive=False,
                    value="Clique em 'Verificar API' para ver o status"
                )
        
        # Event handlers
        def submit_query(query, project_path, file_path):
            if not query.strip():
                return "", "⚠️ Por favor, digite uma pergunta", ""
            
            response, error = query_api(
                query,
                project_path if project_path.strip() else None,
                file_path if file_path.strip() else None,
                stream=False
            )
            
            if error:
                return "", error, response
            else:
                return response, "✅ Resposta gerada com sucesso!", response
        
        def submit_streaming(query, project_path, file_path):
            if not query.strip():
                return "", "⚠️ Por favor, digite uma pergunta", ""
            
            response, status = query_api(
                query,
                project_path if project_path.strip() else None,
                file_path if file_path.strip() else None,
                stream=True
            )
            
            return response, status, response
        
        def send_feedback_handler(query, response, feedback_type, rating):
            if not query.strip() or not response.strip():
                return "⚠️ Preencha query e resposta antes de enviar feedback"
            
            return send_feedback(query, response, feedback_type, int(rating))
        
        def check_health_handler():
            return check_health()
        
        # Bind events
        submit_btn.click(
            fn=submit_query,
            inputs=[query_input, project_path_input, file_path_input],
            outputs=[response_output, status_output, response_output]
        )
        
        stream_btn.click(
            fn=submit_streaming,
            inputs=[query_input, project_path_input, file_path_input],
            outputs=[response_output, status_output, response_output]
        )
        
        feedback_btn.click(
            fn=send_feedback_handler,
            inputs=[query_input, response_output, feedback_type, rating],
            outputs=[feedback_output]
        )
        
        health_btn.click(
            fn=check_health_handler,
            outputs=health_info
        )
        
        # Enter key submits
        query_input.submit(
            fn=submit_query,
            inputs=[query_input, project_path_input, file_path_input],
            outputs=[response_output, status_output, response_output]
        )
    
    return demo


def launch_interface(
    server_name: str = "0.0.0.0",
    server_port: int = 7860,
    share: bool = False
):
    """Inicia interface Gradio"""
    demo = create_interface()
    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=share,
        show_error=True
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Interface web NPLLM")
    parser.add_argument("--port", type=int, default=7860, help="Porta do servidor")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host do servidor")
    parser.add_argument("--api-url", type=str, default="http://localhost:8000", help="URL da API")
    parser.add_argument("--share", action="store_true", help="Criar link público (ngrok)")
    
    args = parser.parse_args()
    
    # Atualiza URL da API se fornecida
    if args.api_url:
        API_URL = args.api_url
    
    launch_interface(
        server_name=args.host,
        server_port=args.port,
        share=args.share
    )

