#!/bin/bash
# Script para iniciar serviços Docker

set -e

echo "=========================================="
echo "🐳 Iniciando Serviços Docker - npllm"
echo "=========================================="
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado!"
    echo "   Instale: sudo apt-get install docker.io"
    exit 1
fi

# Verificar Docker Compose (suporta ambos: docker compose e docker-compose)
DOCKER_COMPOSE_CMD=""
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose não encontrado!"
    echo "   Docker Compose V2: já incluído no Docker"
    echo "   Docker Compose V1: sudo apt-get install docker-compose"
    exit 1
fi

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado"
    if [ -f .env.docker ]; then
        echo "📋 Copiando .env.docker para .env..."
        cp .env.docker .env
        echo "✅ Arquivo .env criado"
    else
        echo "❌ Arquivo .env.docker não encontrado!"
        exit 1
    fi
fi

# Criar diretório de dados se não existir
mkdir -p data/postgres
chmod 700 data/postgres 2>/dev/null || true

# Verificar se container já está rodando
if docker ps | grep -q npllm_postgres; then
    echo "✅ Container já está rodando"
    $DOCKER_COMPOSE_CMD ps
else
    echo "🚀 Iniciando containers..."
    $DOCKER_COMPOSE_CMD up -d
    
    echo ""
    echo "⏳ Aguardando PostgreSQL inicializar..."
    sleep 5
    
    # Verificar saúde
    for i in {1..30}; do
        if $DOCKER_COMPOSE_CMD exec -T postgres pg_isready -U npllm_user -d npllm &> /dev/null; then
            echo "✅ PostgreSQL está pronto!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ Timeout aguardando PostgreSQL"
            exit 1
        fi
        sleep 1
    done
fi

# Criar extensão pgvector
echo ""
echo "🔍 Verificando extensão pgvector..."
$DOCKER_COMPOSE_CMD exec -T postgres psql -U npllm_user -d npllm -c "CREATE EXTENSION IF NOT EXISTS vector;" &> /dev/null

if $DOCKER_COMPOSE_CMD exec -T postgres psql -U npllm_user -d npllm -c "SELECT * FROM pg_extension WHERE extname = 'vector';" | grep -q vector; then
    echo "✅ Extensão pgvector habilitada"
else
    echo "⚠️  Extensão pgvector não encontrada (pode ser normal na primeira vez)"
fi

echo ""
echo "=========================================="
echo "✅ Serviços Docker Iniciados!"
echo "=========================================="
echo ""
echo "📊 Status:"
$DOCKER_COMPOSE_CMD ps
echo ""
echo "📝 Próximos passos:"
echo "   1. Executar teste: python test_real.py"
echo "   2. Ver logs: docker-compose logs -f postgres"
echo "   3. Parar: docker-compose stop"
echo ""

