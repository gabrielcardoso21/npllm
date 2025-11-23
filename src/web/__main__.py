"""
Entry point para interface web: python -m src.web
"""

from src.web.gradio_ui import launch_interface
import sys

if __name__ == "__main__":
    # Lê argumentos da linha de comando
    port = 7860
    host = "0.0.0.0"
    api_url = "http://localhost:8000"
    share = False
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith("--port="):
                port = int(arg.split("=")[1])
            elif arg.startswith("--host="):
                host = arg.split("=")[1]
            elif arg.startswith("--api-url="):
                api_url = arg.split("=")[1]
            elif arg == "--share":
                share = True
    
    # Atualiza URL da API global
    from src.web import gradio_ui
    gradio_ui.API_URL = api_url
    
    print(f"🌐 Iniciando interface web em http://{host}:{port}")
    print(f"🔗 Conectando à API em {api_url}")
    
    launch_interface(
        server_name=host,
        server_port=port,
        share=share
    )

