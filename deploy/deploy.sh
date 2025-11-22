#!/bin/bash
# Script de Deploy para Contabo
# Uso: ./deploy/deploy.sh [server_ip] [user]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuração
SERVER_IP="${1:-161.97.123.192}"
SERVER_USER="${2:-root}"
PROJECT_DIR="/opt/npllm"
REPO_URL="https://github.com/gabrielcardoso21/npllm.git"

echo -e "${GREEN}=========================================="
echo "🚀 Deploy npllm para Contabo"
echo "==========================================${NC}"
echo ""
echo "Servidor: ${SERVER_USER}@${SERVER_IP}"
echo "Diretório: ${PROJECT_DIR}"
echo ""

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Execute este script da raiz do projeto${NC}"
    exit 1
fi

# Verificar conexão SSH
echo -e "${YELLOW}📡 Verificando conexão SSH...${NC}"
if ! ssh -o ConnectTimeout=5 "${SERVER_USER}@${SERVER_IP}" "echo 'Conexão OK'" 2>/dev/null; then
    echo -e "${RED}❌ Não foi possível conectar ao servidor${NC}"
    echo "   Verifique:"
    echo "   - SSH configurado corretamente"
    echo "   - Chave SSH adicionada ao servidor"
    echo "   - IP e usuário corretos"
    exit 1
fi
echo -e "${GREEN}✅ Conexão SSH OK${NC}"
echo ""

# Executar setup no servidor
echo -e "${YELLOW}🔧 Executando setup no servidor...${NC}"
ssh "${SERVER_USER}@${SERVER_IP}" bash << 'ENDSSH'
set -e

PROJECT_DIR="/opt/npllm"
REPO_URL="https://github.com/gabrielcardoso21/npllm.git"

# Criar diretório se não existir
mkdir -p "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

# Clonar ou atualizar repositório
if [ -d ".git" ]; then
    echo "📥 Atualizando repositório..."
    git pull origin main || git pull origin master
else
    echo "📥 Clonando repositório..."
    git clone "${REPO_URL}" .
fi

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "🐍 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar e instalar dependências
echo "📦 Instalando dependências..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Criar diretórios necessários
mkdir -p data/postgres logs models/cache models/embeddings_cache

# Configurar permissões
chmod +x INICIAR_DOCKER.sh
chmod +x deploy/setup_production.sh

echo "✅ Setup concluído no servidor"
ENDSSH

echo -e "${GREEN}✅ Deploy concluído!${NC}"
echo ""
echo "Próximos passos:"
echo "1. SSH no servidor: ssh ${SERVER_USER}@${SERVER_IP}"
echo "2. Execute: cd ${PROJECT_DIR} && ./deploy/setup_production.sh"
echo "3. Configure variáveis de ambiente: nano .env"
echo "4. Inicie serviços: ./INICIAR_DOCKER.sh"
echo ""

