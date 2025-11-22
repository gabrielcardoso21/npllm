#!/bin/bash
# Setup script for PostgreSQL + pgvector
# Optimized for low memory usage (4 vCPU + 8GB RAM)

set -e

echo "Setting up PostgreSQL + pgvector for npllm..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install it first."
    exit 1
fi

# Create database and user
echo "Creating database and user..."
sudo -u postgres psql <<EOF
CREATE DATABASE npllm;
CREATE USER npllm_user WITH PASSWORD 'npllm_password';
GRANT ALL PRIVILEGES ON DATABASE npllm TO npllm_user;
\c npllm
CREATE EXTENSION IF NOT EXISTS vector;
GRANT ALL ON SCHEMA public TO npllm_user;
EOF

# Configure PostgreSQL for low memory usage
echo "Configuring PostgreSQL for low memory usage..."
PG_VERSION=$(psql --version | grep -oP '\d+' | head -1)
PG_CONFIG="/etc/postgresql/${PG_VERSION}/main/postgresql.conf"

if [ -f "$PG_CONFIG" ]; then
    sudo sed -i "s/#shared_buffers = 128MB/shared_buffers = 256MB/" "$PG_CONFIG"
    sudo sed -i "s/#effective_cache_size = 4GB/effective_cache_size = 1GB/" "$PG_CONFIG"
    sudo sed -i "s/#work_mem = 4MB/work_mem = 16MB/" "$PG_CONFIG"
    sudo sed -i "s/#maintenance_work_mem = 64MB/maintenance_work_mem = 128MB/" "$PG_CONFIG"
    
    echo "PostgreSQL configuration updated. Restart PostgreSQL to apply changes:"
    echo "sudo systemctl restart postgresql"
else
    echo "Warning: Could not find PostgreSQL config file. Please configure manually."
fi

echo "Setup complete!"
echo "Database: npllm"
echo "User: npllm_user"
echo "Password: npllm_password (change this in production!)"

