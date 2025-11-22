#!/bin/bash
# Script de Setup de Produção
# Execute no servidor após o deploy

set -e

echo "=========================================="
echo "🔧 Setup de Produção - npllm"
echo "=========================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Execute este script da raiz do projeto"
    exit 1
fi

# 1. Instalar dependências do sistema
echo "📦 Instalando dependências do sistema..."
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    docker.io \
    docker-compose \
    git \
    curl \
    build-essential

# 2. Configurar Docker (se necessário)
if ! groups | grep -q docker; then
    echo "🔐 Adicionando usuário ao grupo docker..."
    sudo usermod -aG docker $USER
    echo "⚠️  Você precisa fazer logout/login para aplicar as mudanças"
fi

# 3. Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cat > .env << 'EOF'
# Database (Docker Compose)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=npllm
DB_USER=npllm_user
DB_PASSWORD=npllm_password_change_me

# Model (opcional - usa defaults se não especificar)
MODEL_BASE_MODEL=codellama/CodeLlama-3b-Instruct-hf
MODEL_DEVICE=cpu
MODEL_MAX_MEMORY=6GB
EOF
    echo "✅ Arquivo .env criado"
    echo "⚠️  IMPORTANTE: Edite .env e altere DB_PASSWORD!"
else
    echo "✅ Arquivo .env já existe"
fi

# 4. Criar diretórios
echo "📁 Criando diretórios..."
mkdir -p data/postgres logs models/cache models/embeddings_cache
chmod 700 data/postgres

# 5. Configurar systemd service (opcional)
if [ ! -f /etc/systemd/system/npllm.service ]; then
    echo "⚙️  Criando serviço systemd..."
    sudo tee /etc/systemd/system/npllm.service > /dev/null << EOF
[Unit]
Description=npllm - NeuroPlastic Large Language Model
After=network.target docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/INICIAR_DOCKER.sh
ExecStop=docker-compose -f $(pwd)/docker-compose.yml down
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOF
    echo "✅ Serviço systemd criado"
    echo "   Para habilitar: sudo systemctl enable npllm"
    echo "   Para iniciar: sudo systemctl start npllm"
fi

# 6. Iniciar Docker Compose
echo "🐳 Iniciando Docker Compose..."
./INICIAR_DOCKER.sh

echo ""
echo "=========================================="
echo "✅ Setup de Produção Concluído!"
echo "=========================================="
echo ""
echo "Próximos passos:"
echo "1. Edite .env e configure senhas: nano .env"
echo "2. Teste o sistema: source .venv/bin/activate && python test_real.py"
echo "3. (Opcional) Habilite serviço systemd: sudo systemctl enable npllm"
echo ""

