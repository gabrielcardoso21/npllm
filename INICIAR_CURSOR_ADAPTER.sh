#!/bin/bash
# Script para iniciar o adapter do Cursor

set -e

echo "🚀 Iniciando npllm Cursor Adapter..."
echo ""

# Ativa ambiente virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Carrega variáveis de ambiente
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Inicia adapter na porta 8001 (para não conflitar com API principal)
echo "📡 Adapter rodando em: http://localhost:8001"
echo "🔌 Endpoint: http://localhost:8001/v1/chat/completions"
echo ""
echo "💡 Configure o Cursor para usar:"
echo "   Base URL: http://localhost:8001"
echo "   Model: npllm"
echo ""
echo "⚠️  Pressione Ctrl+C para parar"
echo ""

python3 -m src.api.cursor_adapter

