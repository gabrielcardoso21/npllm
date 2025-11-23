#!/bin/bash
# Script para iniciar interface web Gradio

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌐 Iniciando Interface Web NPLLM${NC}"

# Ativa ambiente virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✅ Ambiente virtual ativado${NC}"
else
    echo "❌ Ambiente virtual não encontrado. Execute: python3 -m venv .venv"
    exit 1
fi

# Verifica se API está rodando
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${BLUE}⚠️  API não está rodando. Inicie com: python3 -m src.api.server${NC}"
    echo -e "${BLUE}   Ou execute: ./INICIAR_API.sh${NC}"
    read -p "Deseja continuar mesmo assim? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Porta padrão
PORT=${1:-7860}
API_URL=${2:-http://localhost:8000}

echo -e "${GREEN}🚀 Iniciando interface web na porta ${PORT}${NC}"
echo -e "${GREEN}🔗 Conectando à API em ${API_URL}${NC}"
echo ""
echo -e "${BLUE}📖 Acesse: http://localhost:${PORT}${NC}"
echo ""

# Inicia interface
python3 -m src.web --port=$PORT --api-url=$API_URL

