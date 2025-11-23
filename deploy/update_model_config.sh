#!/bin/bash
# Script para atualizar configuração do modelo no servidor remoto

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Atualizando Configuração do Modelo${NC}"

# Verifica argumentos
if [ $# -lt 2 ]; then
    echo "Uso: $0 <IP_SERVIDOR> <USUARIO>"
    echo "Exemplo: $0 161.97.123.192 root"
    exit 1
fi

SERVER_IP=$1
SERVER_USER=$2

echo -e "${BLUE}   Servidor: ${SERVER_USER}@${SERVER_IP}${NC}"
echo ""

# Atualiza configuração no servidor
ssh "${SERVER_USER}@${SERVER_IP}" << 'EOF'
cd /opt/npllm

echo "📋 Verificando configuração atual..."
if [ -f config/default.yaml ]; then
    echo "✅ config/default.yaml encontrado"
    grep "base_model" config/default.yaml | head -1
fi

if [ -f config/production.yaml ]; then
    echo "✅ config/production.yaml encontrado"
    grep "base_model" config/production.yaml | head -1
fi

echo ""
echo "🔄 Atualizando para TinyLlama..."

# Atualiza default.yaml
if [ -f config/default.yaml ]; then
    sed -i 's|base_model:.*|base_model: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Modelo menor para testes|' config/default.yaml
    sed -i 's|max_memory:.*|max_memory: "2GB"  # Reduzido para modelo menor|' config/default.yaml
    echo "✅ config/default.yaml atualizado"
fi

# Atualiza production.yaml
if [ -f config/production.yaml ]; then
    sed -i 's|base_model:.*|base_model: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Modelo menor para testes|' config/production.yaml
    sed -i 's|max_memory:.*|max_memory: "2GB"  # Reduzido para modelo menor|' config/production.yaml
    echo "✅ config/production.yaml atualizado"
fi

echo ""
echo "📋 Nova configuração:"
grep -A 1 "base_model" config/default.yaml | head -2

echo ""
echo "⚠️  IMPORTANTE: Reinicie a API para aplicar as mudanças:"
echo "   pkill -f src.api.server"
echo "   ./deploy/start_api.sh"
EOF

echo ""
echo -e "${GREEN}✅ Configuração atualizada!${NC}"
echo -e "${YELLOW}⚠️  Não esqueça de reiniciar a API no servidor${NC}"

