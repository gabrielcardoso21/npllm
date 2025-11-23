#!/bin/bash
# Script para iniciar interface web Gradio no servidor Contabo

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌐 Iniciando Interface Web NPLLM${NC}"

# Diretório do projeto
PROJECT_DIR="/opt/npllm"
cd "$PROJECT_DIR"

# Ativa ambiente virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✅ Ambiente virtual ativado${NC}"
else
    echo "❌ Ambiente virtual não encontrado em $PROJECT_DIR/.venv"
    exit 1
fi

# Verifica se API está rodando
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  API não está rodando em http://localhost:8000${NC}"
    echo -e "${YELLOW}   Inicie a API primeiro com: ./deploy/start_api.sh${NC}"
    read -p "Deseja continuar mesmo assim? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Porta padrão (pode ser passada como argumento)
PORT=${1:-7860}
API_URL=${2:-http://localhost:8000}

# Para processo anterior se existir
if pgrep -f "src.web" > /dev/null; then
    echo -e "${YELLOW}⚠️  Processo anterior encontrado, parando...${NC}"
    pkill -f "src.web"
    sleep 2
fi

# Verifica se porta está em uso
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Porta $PORT já está em uso${NC}"
    read -p "Deseja usar outra porta? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        read -p "Digite a nova porta: " PORT
    else
        exit 1
    fi
fi

echo -e "${GREEN}🚀 Iniciando interface web na porta ${PORT}${NC}"
echo -e "${GREEN}🔗 Conectando à API em ${API_URL}${NC}"
echo -e "${GREEN}📖 Acesse: http://$(hostname -I | awk '{print $1}'):${PORT}${NC}"
echo ""

# Inicia interface em background
nohup python3 -m src.web \
    --port=$PORT \
    --host=0.0.0.0 \
    --api-url=$API_URL \
    > /var/log/npllm_web.log 2>&1 &

# Aguarda alguns segundos
sleep 5

# Verifica se iniciou
if pgrep -f "src.web" > /dev/null; then
    PID=$(pgrep -f "src.web")
    echo -e "${GREEN}✅ Interface web iniciada (PID: $PID)${NC}"
    echo -e "${BLUE}📋 Logs: tail -f /var/log/npllm_web.log${NC}"
    echo -e "${BLUE}🛑 Parar: pkill -f 'src.web'${NC}"
else
    echo -e "${YELLOW}⚠️  Interface web pode não ter iniciado corretamente${NC}"
    echo -e "${YELLOW}   Verifique os logs: tail -20 /var/log/npllm_web.log${NC}"
    exit 1
fi

