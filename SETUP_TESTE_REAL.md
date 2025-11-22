# Setup para Teste Real

**Data**: 2025-01-27

---

## 📋 Pré-requisitos

### 1. PostgreSQL com pgvector

```bash
# Instalar PostgreSQL (se não tiver)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Instalar pgvector
# Opção 1: Via apt (se disponível)
sudo apt-get install postgresql-14-pgvector  # Ajuste a versão

# Opção 2: Via extensão (recomendado)
# Conecte ao PostgreSQL e execute:
# CREATE EXTENSION vector;
```

**Configurar banco de dados**:

```bash
# Criar usuário e banco
sudo -u postgres psql

# No psql:
CREATE DATABASE npllm;
CREATE USER npllm_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE npllm TO npllm_user;
\c npllm
CREATE EXTENSION vector;
\q
```

### 2. Variáveis de Ambiente

Crie arquivo `.env` na raiz do projeto:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=npllm
DB_USER=npllm_user
DB_PASSWORD=sua_senha_aqui

# Model (opcional - usa defaults se não especificar)
MODEL_BASE_MODEL=codellama/CodeLlama-3b-Instruct-hf
MODEL_DEVICE=cpu
```

### 3. Dependências Python

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Instalar pgvector Python (se necessário)
pip install pgvector
```

### 4. Modelos

O sistema baixará automaticamente:
- **CodeLlama 3B** (base model)
- **RoBERTa** (sentiment analysis)

**Nota**: Primeira execução pode demorar para baixar modelos.

---

## 🚀 Executar Teste Real

### Opção 1: Script de Teste Completo

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar teste
python test_real.py
```

### Opção 2: Via CLI do Sistema

```bash
# Query simples
python -m src.main --query "Create a hello function in Python"

# Analisar projeto
python -m src.main --analyze /path/to/project

# Acionar sono manualmente
python -m src.main --sleep
```

---

## ✅ Checklist Antes de Testar

- [ ] PostgreSQL instalado e rodando
- [ ] pgvector instalado e habilitado
- [ ] Banco de dados `npllm` criado
- [ ] Usuário `npllm_user` criado com permissões
- [ ] Extensão `vector` criada no banco
- [ ] Variáveis de ambiente configuradas (`.env`)
- [ ] Dependências Python instaladas
- [ ] Ambiente virtual ativado

---

## 🔍 Verificar Configuração

### Testar Conexão PostgreSQL

```bash
psql -h localhost -U npllm_user -d npllm -c "SELECT 1;"
```

### Verificar pgvector

```bash
psql -h localhost -U npllm_user -d npllm -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### Verificar Modelos

O sistema tentará baixar modelos automaticamente na primeira execução.

---

## ⚠️ Problemas Comuns

### 1. Erro: "vector type not found"

**Solução**: Instalar e habilitar extensão pgvector:
```sql
CREATE EXTENSION vector;
```

### 2. Erro: "Connection refused"

**Solução**: Verificar se PostgreSQL está rodando:
```bash
sudo systemctl status postgresql
```

### 3. Erro: "Module not found"

**Solução**: Instalar dependências:
```bash
pip install -r requirements.txt
```

### 4. Erro: "Model not found"

**Solução**: Primeira execução baixa modelos automaticamente. Aguarde.

---

## 📊 O Que Esperar

O teste real executará:

1. ✅ **Inicialização do sistema** (~30-60s na primeira vez)
2. ✅ **Query básica** (gera código Python)
3. ✅ **Captura de feedback** (armazena no PostgreSQL)
4. ✅ **Análise de projeto** (identifica padrões)
5. ✅ **Consolidação (sono)** (fine-tuning de adapters)
6. ✅ **Status do sistema** (verifica saúde)

**Tempo estimado**: 2-5 minutos (depende do hardware)

---

**Última Atualização**: 2025-01-27

