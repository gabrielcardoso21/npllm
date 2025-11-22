#!/bin/bash
# Script para iniciar API no servidor Contabo

set -e

cd /opt/npllm

echo "=========================================="
echo "🚀 Iniciando API npllm no servidor"
echo "=========================================="
echo ""

# Verificar ambiente virtual
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual não encontrado"
    exit 1
fi

# Ativar ambiente virtual
source .venv/bin/activate

# Verificar se PostgreSQL está rodando
if ! docker ps | grep -q npllm_postgres; then
    echo "⚠️  PostgreSQL não está rodando"
    echo "   Iniciando PostgreSQL..."
    docker compose up -d postgres
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
echo "   Docs: http://$(hostname -I | awk '{print $1}'):8000/docs"
echo ""

# Usar nohup para rodar em background
nohup python -m src.api.server --host 0.0.0.0 --port 8000 > /var/log/npllm_api.log 2>&1 &

echo "✅ API iniciada em background"
echo "   PID: $!"
echo "   Logs: /var/log/npllm_api.log"
echo ""
echo "Para parar: pkill -f 'src.api.server'"

