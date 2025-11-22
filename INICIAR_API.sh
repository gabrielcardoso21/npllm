#!/bin/bash
# Script para iniciar API do npllm

set -e

echo "=========================================="
echo "🚀 Iniciando API npllm"
echo "=========================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Execute este script da raiz do projeto"
    exit 1
fi

# Verificar ambiente virtual
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual não encontrado"
    echo "   Execute: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Ativar ambiente virtual
source .venv/bin/activate

# Verificar se PostgreSQL está rodando
if ! docker ps | grep -q npllm_postgres; then
    echo "⚠️  PostgreSQL não está rodando"
    echo "   Iniciando PostgreSQL..."
    ./INICIAR_DOCKER.sh
    sleep 5
fi

# Verificar variáveis de ambiente
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado"
    if [ -f .env.docker ]; then
        echo "📋 Copiando .env.docker para .env..."
        cp .env.docker .env
    else
        echo "❌ Arquivo .env.docker não encontrado!"
        exit 1
    fi
fi

# Iniciar API
echo "🌐 Iniciando servidor API..."
echo "   Host: 0.0.0.0"
echo "   Port: 8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

python -m src.api.server

