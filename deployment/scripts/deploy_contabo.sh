#!/bin/bash
# Deployment script for Contabo servers
# Optimized for 4 vCPU + 8GB RAM

set -e

echo "Deploying npllm to Contabo server..."

# Configuration
SERVER_IP="${CONTABO_IP:-161.97.123.192}"
SERVER_USER="${CONTABO_USER:-root}"
DEPLOY_DIR="/opt/npllm"

# Check if server is accessible
echo "Checking server connection..."
ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_IP} "echo 'Connection successful'"

# Create deployment directory
echo "Creating deployment directory..."
ssh ${SERVER_USER}@${SERVER_IP} "mkdir -p ${DEPLOY_DIR}"

# Copy files
echo "Copying files..."
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' \
    --exclude '.git' --exclude 'models/*.bin' --exclude 'models/*.pt' \
    ./ ${SERVER_USER}@${SERVER_IP}:${DEPLOY_DIR}/

# Install dependencies
echo "Installing dependencies..."
ssh ${SERVER_USER}@${SERVER_IP} "cd ${DEPLOY_DIR} && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"

# Setup PostgreSQL (if needed)
echo "Setting up PostgreSQL..."
ssh ${SERVER_USER}@${SERVER_IP} "cd ${DEPLOY_DIR} && bash deployment/scripts/setup_postgres.sh || true"

# Create systemd service
echo "Creating systemd service..."
ssh ${SERVER_USER}@${SERVER_IP} "cat > /etc/systemd/system/npllm.service <<EOF
[Unit]
Description=NeuroPlastic Large Language Model
After=network.target postgresql.service

[Service]
Type=simple
User=npllm
WorkingDirectory=${DEPLOY_DIR}
Environment=\"PATH=${DEPLOY_DIR}/venv/bin\"
ExecStart=${DEPLOY_DIR}/venv/bin/python -m src.main --config config/production.yaml
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

# Enable and start service
echo "Starting service..."
ssh ${SERVER_USER}@${SERVER_IP} "systemctl daemon-reload && systemctl enable npllm && systemctl start npllm"

echo "Deployment completed!"
echo "Service status:"
ssh ${SERVER_USER}@${SERVER_IP} "systemctl status npllm"

