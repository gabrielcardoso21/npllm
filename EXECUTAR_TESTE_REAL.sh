#!/bin/bash
# Script para executar teste real do sistema npllm

set -e

echo "=========================================="
echo "🚀 Teste Real - Sistema npllm"
echo "=========================================="
echo ""

# Verificar ambiente virtual
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "   Execute: python3 -m venv .venv"
    exit 1
fi

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source .venv/bin/activate

# Verificar dependências
echo "🔍 Verificando dependências..."
python -c "import torch; import transformers; import psycopg2; print('✅ Dependências OK')" || {
    echo "❌ Dependências faltando!"
    echo "   Execute: pip install -r requirements.txt"
    exit 1
}

# Verificar PostgreSQL (Docker ou local)
echo "🔍 Verificando PostgreSQL..."
if docker ps | grep -q npllm_postgres; then
    echo "✅ PostgreSQL rodando no Docker"
    # Tentar docker compose primeiro, depois docker-compose
    if docker compose exec -T postgres psql -U npllm_user -d npllm -c "SELECT 1;" 2>/dev/null || \
       docker-compose exec -T postgres psql -U npllm_user -d npllm -c "SELECT 1;" 2>/dev/null; then
        echo "✅ PostgreSQL conectado (Docker)"
    else
        echo "⚠️  PostgreSQL Docker não respondeu (continuando mesmo assim)"
    fi
elif psql -h localhost -U npllm_user -d npllm -c "SELECT 1;" 2>/dev/null; then
    echo "✅ PostgreSQL conectado (local)"
else
    echo "⚠️  PostgreSQL não encontrado"
    echo "   Opção 1: Iniciar Docker: ./INICIAR_DOCKER.sh"
    echo "   Opção 2: Instalar local: SETUP_TESTE_REAL.md"
fi

# Executar teste
echo ""
echo "▶️  Executando teste real..."
echo ""

python test_real.py

echo ""
echo "✅ Teste concluído!"

