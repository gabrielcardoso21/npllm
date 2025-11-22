"""
API Server Entry Point
"""

import sys
import os

# Adicionar raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import argparse
from src.api.server import run_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="npllm API Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)
