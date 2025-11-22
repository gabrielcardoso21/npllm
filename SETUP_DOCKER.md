# 🐳 Setup com Docker Compose

**Data**: 2025-01-27

---

## 📋 Pré-requisitos

### Docker e Docker Compose

```bash
# Verificar se já está instalado
docker --version
docker-compose --version

# Se não estiver instalado:
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Ou instalar Docker Desktop (recomendado)
# https://www.docker.com/products/docker-desktop
```

---

## 🚀 Setup Rápido

### 1. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.docker .env

# Ou criar manualmente
cat > .env << EOF
DB_HOST=localhost
DB_PORT=5432
DB_NAME=npllm
DB_USER=npllm_user
DB_PASSWORD=npllm_password
EOF
```

### 2. Iniciar PostgreSQL

```bash
# Iniciar container
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f postgres
```

### 3. Verificar Conexão

```bash
# Testar conexão
docker-compose exec postgres psql -U npllm_user -d npllm -c "SELECT version();"

# Verificar extensão pgvector
docker-compose exec postgres psql -U npllm_user -d npllm -c "CREATE EXTENSION IF NOT EXISTS vector;"
docker-compose exec postgres psql -U npllm_user -d npllm -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### 4. Executar Sistema

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar teste
python test_real.py
```

---

## 🛠️ Comandos Úteis

### Gerenciar Container

```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose stop

# Parar e remover
docker-compose down

# Parar e remover volumes (APAGA DADOS!)
docker-compose down -v

# Ver logs
docker-compose logs -f postgres

# Reiniciar
docker-compose restart postgres
```

### Acessar PostgreSQL

```bash
# Via docker-compose
docker-compose exec postgres psql -U npllm_user -d npllm

# Via psql local (se tiver instalado)
psql -h localhost -U npllm_user -d npllm
```

### Backup e Restore

```bash
# Backup
docker-compose exec postgres pg_dump -U npllm_user npllm > backup.sql

# Restore
docker-compose exec -T postgres psql -U npllm_user npllm < backup.sql
```

---

## 📊 Verificar Recursos Docker

```bash
# Ver uso de recursos
docker stats npllm_postgres

# Ver espaço usado
docker system df
```

---

## ⚠️ Problemas Comuns

### 1. Porta 5432 já em uso

**Solução**: Alterar porta no `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Usa 5433 localmente
```

E atualizar `.env`:
```
DB_PORT=5433
```

### 2. Container não inicia

**Solução**: Verificar logs
```bash
docker-compose logs postgres
```

### 3. Permissões negadas

**Solução**: Adicionar usuário ao grupo docker
```bash
sudo usermod -aG docker $USER
# Fazer logout e login novamente
```

### 4. Volume não persiste

**Solução**: Verificar volumes
```bash
docker volume ls
docker volume inspect npllm_postgres_data
```

---

## 🔧 Configuração Avançada

### Ajustar Memória do PostgreSQL

Editar `docker-compose.yml`:
```yaml
services:
  postgres:
    environment:
      POSTGRES_SHARED_BUFFERS: 256MB
      POSTGRES_EFFECTIVE_CACHE_SIZE: 1GB
      POSTGRES_WORK_MEM: 16MB
```

### Usar Versão Específica do PostgreSQL

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg15  # ou pg14, pg13
```

### Adicionar Outros Serviços

```yaml
services:
  postgres:
    # ... configuração existente
  
  redis:  # Exemplo: adicionar Redis
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - npllm_network
```

---

## 📝 Checklist

- [ ] Docker instalado
- [ ] Docker Compose instalado
- [ ] Arquivo `.env` criado
- [ ] Container iniciado: `docker-compose up -d`
- [ ] Extensão pgvector criada
- [ ] Conexão testada
- [ ] Sistema executado com sucesso

---

## 🎯 Vantagens do Docker

✅ **Isolamento**: Não polui sistema local  
✅ **Fácil remoção**: `docker-compose down -v`  
✅ **Portabilidade**: Funciona em qualquer máquina  
✅ **Versões específicas**: pgvector pré-configurado  
✅ **Sem instalação local**: Não precisa instalar PostgreSQL  

---

**Última Atualização**: 2025-01-27

