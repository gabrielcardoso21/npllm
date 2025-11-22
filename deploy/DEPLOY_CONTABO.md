# 🚀 Deploy no Contabo

**Data**: 2025-01-27  
**Servidores Disponíveis**: 
- 161.97.123.192
- 207.244.252.217

---

## 📋 Pré-requisitos

### Local (Sua Máquina)

- Git instalado
- SSH configurado com acesso aos servidores Contabo
- Chave SSH adicionada ao servidor

### Servidor Contabo

- Ubuntu 20.04+ ou Debian 11+
- Acesso root ou usuário com sudo
- Pelo menos 8GB RAM, 4 vCPU
- 50GB+ espaço em disco

---

## 🚀 Deploy Automatizado

### Opção 1: Deploy Rápido (Recomendado)

```bash
# Na sua máquina, da raiz do projeto
chmod +x deploy/deploy.sh
./deploy/deploy.sh [IP_SERVIDOR] [USUARIO]

# Exemplo:
./deploy/deploy.sh 161.97.123.192 root
```

O script irá:
1. Verificar conexão SSH
2. Clonar/atualizar repositório no servidor
3. Criar ambiente virtual
4. Instalar dependências Python

### Opção 2: Deploy Manual

```bash
# 1. Conectar ao servidor
ssh root@161.97.123.192

# 2. Clonar repositório
cd /opt
git clone https://github.com/gabrielcardoso21/npllm.git
cd npllm

# 3. Executar setup de produção
chmod +x deploy/setup_production.sh
./deploy/setup_production.sh
```

---

## ⚙️ Configuração Pós-Deploy

### 1. Configurar Variáveis de Ambiente

```bash
# No servidor
cd /opt/npllm
nano .env
```

Edite as seguintes variáveis:

```bash
# Database (IMPORTANTE: Altere a senha!)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=npllm
DB_USER=npllm_user
DB_PASSWORD=senha_segura_aqui  # ⚠️ ALTERE ISSO!

# Model (opcional)
MODEL_BASE_MODEL=codellama/CodeLlama-3b-Instruct-hf
MODEL_DEVICE=cpu
MODEL_MAX_MEMORY=6GB
```

### 2. Iniciar Serviços

```bash
# Iniciar PostgreSQL via Docker
./INICIAR_DOCKER.sh

# Verificar status
docker-compose ps
```

### 3. Testar Sistema

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar teste
python test_real.py
```

---

## 🔧 Configuração como Serviço (Opcional)

Para rodar o sistema como serviço systemd:

```bash
# Habilitar serviço (inicia automaticamente no boot)
sudo systemctl enable npllm

# Iniciar serviço
sudo systemctl start npllm

# Verificar status
sudo systemctl status npllm

# Ver logs
sudo journalctl -u npllm -f
```

---

## 📊 Monitoramento

### Verificar Status dos Containers

```bash
docker-compose ps
docker-compose logs -f postgres
```

### Verificar Uso de Recursos

```bash
# CPU e Memória
htop

# Disco
df -h

# Docker
docker stats
```

### Verificar Logs do Sistema

```bash
# Logs do npllm
tail -f logs/npllm.log

# Logs do PostgreSQL
docker-compose logs -f postgres
```

---

## 🔄 Atualização

Para atualizar o sistema:

```bash
# No servidor
cd /opt/npllm

# Atualizar código
git pull origin main

# Atualizar dependências
source .venv/bin/activate
pip install -r requirements.txt

# Reiniciar serviços (se usando systemd)
sudo systemctl restart npllm

# Ou manualmente
docker-compose restart
```

---

## 💾 Backup e Restore

### Backup do Banco de Dados

```bash
# Backup
docker-compose exec postgres pg_dump -U npllm_user npllm > backup_$(date +%Y%m%d).sql

# Backup completo (incluindo dados)
tar -czf backup_completo_$(date +%Y%m%d).tar.gz \
    data/postgres \
    models/cache \
    .env \
    config/
```

### Restore

```bash
# Restore do banco
docker-compose exec -T postgres psql -U npllm_user npllm < backup_20250127.sql

# Restore completo
tar -xzf backup_completo_20250127.tar.gz
```

---

## 🔒 Segurança

### 1. Firewall

```bash
# Permitir apenas portas necessárias
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 5432/tcp  # PostgreSQL (apenas se necessário acesso externo)
sudo ufw enable
```

**Nota**: Por padrão, PostgreSQL só aceita conexões locais. Se precisar acesso externo, configure adequadamente.

### 2. Senhas Fortes

- Use senhas fortes para `DB_PASSWORD`
- Considere usar variáveis de ambiente ou secrets manager
- Não commite `.env` no Git

### 3. SSL/TLS (Futuro)

Para produção, considere:
- SSL para PostgreSQL
- HTTPS para APIs (se implementar)
- Certificados Let's Encrypt

---

## 🐛 Troubleshooting

### PostgreSQL não inicia

```bash
# Ver logs
docker-compose logs postgres

# Verificar permissões
ls -la data/postgres

# Recriar container
docker-compose down
docker-compose up -d
```

### Erro de conexão

```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Testar conexão
docker-compose exec postgres psql -U npllm_user -d npllm -c "SELECT 1;"
```

### Erro de memória

```bash
# Verificar uso
free -h
docker stats

# Ajustar limites no docker-compose.yml se necessário
```

### Modelos não baixam

```bash
# Verificar espaço em disco
df -h

# Verificar cache do HuggingFace
ls -lh ~/.cache/huggingface/

# Limpar cache se necessário
rm -rf ~/.cache/huggingface/transformers/
```

---

## 📝 Checklist de Deploy

- [ ] Servidor acessível via SSH
- [ ] Repositório clonado/atualizado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Arquivo `.env` configurado
- [ ] PostgreSQL rodando (Docker)
- [ ] Extensão pgvector habilitada
- [ ] Teste básico executado com sucesso
- [ ] (Opcional) Serviço systemd configurado
- [ ] (Opcional) Firewall configurado
- [ ] Backup inicial realizado

---

## 🔗 Links Úteis

- [Documentação Docker](https://docs.docker.com/)
- [Documentação PostgreSQL](https://www.postgresql.org/docs/)
- [Documentação pgvector](https://github.com/pgvector/pgvector)
- [Contabo Knowledge Base](https://contabo.com/en/knowledge-base/)

---

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs: `docker-compose logs -f`
2. Verifique o status: `docker-compose ps`
3. Consulte a documentação: `docs/`
4. Verifique issues no GitHub

