#!/bin/bash
# Script para fazer deploy completo incluindo interface web

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica argumentos
if [ $# -lt 2 ]; then
    echo "Uso: $0 <IP_SERVIDOR> <USUARIO>"
    echo "Exemplo: $0 161.97.123.192 root"
    exit 1
fi

SERVER_IP=$1
SERVER_USER=$2

echo -e "${BLUE}🚀 Deploy completo NPLLM (API + Interface Web)${NC}"
echo -e "${BLUE}   Servidor: ${SERVER_USER}@${SERVER_IP}${NC}"
echo ""

# 1. Deploy base (código)
echo -e "${GREEN}1️⃣  Fazendo deploy do código...${NC}"
./deploy/deploy.sh "$SERVER_IP" "$SERVER_USER"

# 2. Instalar dependências (incluindo Gradio)
echo -e "${GREEN}2️⃣  Instalando dependências (incluindo Gradio)...${NC}"
ssh "${SERVER_USER}@${SERVER_IP}" << 'EOF'
cd /opt/npllm
source .venv/bin/activate
pip install gradio>=4.44.0 --quiet
echo "✅ Dependências instaladas"
EOF

# 3. Iniciar API (se não estiver rodando)
echo -e "${GREEN}3️⃣  Verificando API...${NC}"
ssh "${SERVER_USER}@${SERVER_IP}" << 'EOF'
cd /opt/npllm
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  API não está rodando, iniciando..."
    ./deploy/start_api.sh
    sleep 10
else
    echo "✅ API já está rodando"
fi
EOF

# 4. Iniciar Interface Web
echo -e "${GREEN}4️⃣  Iniciando Interface Web...${NC}"
ssh "${SERVER_USER}@${SERVER_IP}" << 'EOF'
cd /opt/npllm
./deploy/start_web.sh 7860 http://localhost:8000
EOF

echo ""
echo -e "${GREEN}✅ Deploy completo!${NC}"
echo -e "${BLUE}📖 API: http://${SERVER_IP}:8000${NC}"
echo -e "${BLUE}🌐 Interface Web: http://${SERVER_IP}:7860${NC}"
echo ""
echo -e "${YELLOW}📋 Comandos úteis:${NC}"
echo -e "   Ver logs API: ssh ${SERVER_USER}@${SERVER_IP} 'tail -f /var/log/npllm_api.log'"
echo -e "   Ver logs Web: ssh ${SERVER_USER}@${SERVER_IP} 'tail -f /var/log/npllm_web.log'"
echo -e "   Parar API: ssh ${SERVER_USER}@${SERVER_IP} 'pkill -f src.api.server'"
echo -e "   Parar Web: ssh ${SERVER_USER}@${SERVER_IP} 'pkill -f src.web'"

