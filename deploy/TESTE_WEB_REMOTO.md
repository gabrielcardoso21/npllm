# 🧪 Teste da Interface Web no Servidor Remoto

## 📋 Checklist Antes de Testar

- [ ] Código atualizado no servidor (`git pull`)
- [ ] Dependências instaladas (incluindo Gradio)
- [ ] API rodando (`http://localhost:8000`)
- [ ] PostgreSQL rodando
- [ ] Porta 7860 disponível

## 🚀 Deploy Rápido

### Opção 1: Deploy Completo (Recomendado)
```bash
./deploy/deploy_web.sh 161.97.123.192 root
```

Este script:
1. Faz deploy do código
2. Instala dependências (incluindo Gradio)
3. Inicia API (se não estiver rodando)
4. Inicia Interface Web

### Opção 2: Deploy Manual

```bash
# 1. Deploy código
./deploy/deploy.sh 161.97.123.192 root

# 2. SSH no servidor
ssh root@161.97.123.192

# 3. No servidor:
cd /opt/npllm
git pull
source .venv/bin/activate
pip install gradio>=4.44.0

# 4. Iniciar API (se não estiver rodando)
./deploy/start_api.sh

# 5. Iniciar Interface Web
./deploy/start_web.sh 7860 http://localhost:8000
```

## ✅ Verificar Status

### No Servidor
```bash
# Verificar processos
ps aux | grep -E "(src.api.server|src.web)"

# Verificar portas
netstat -tlnp | grep -E "(8000|7860)"
# ou
ss -tlnp | grep -E "(8000|7860)"

# Ver logs
tail -f /var/log/npllm_api.log
tail -f /var/log/npllm_web.log
```

### Do Local
```bash
# Testar API
curl http://161.97.123.192:8000/health

# Testar Interface Web
curl http://161.97.123.192:7860
```

## 🌐 Acessar Interface

Abra no navegador:
```
http://161.97.123.192:7860
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'gradio'"
```bash
ssh root@161.97.123.192
cd /opt/npllm
source .venv/bin/activate
pip install gradio>=4.44.0
```

### Erro: "Connection refused" na API
```bash
# Verificar se API está rodando
curl http://localhost:8000/health

# Iniciar API
./deploy/start_api.sh
```

### Erro: "Port already in use"
```bash
# Verificar processo na porta
lsof -i :7860
# ou
ss -tlnp | grep 7860

# Parar processo anterior
pkill -f src.web

# Usar outra porta
./deploy/start_web.sh 7861 http://localhost:8000
```

### Interface não carrega
1. Verificar logs: `tail -50 /var/log/npllm_web.log`
2. Verificar se API está acessível: `curl http://localhost:8000/health`
3. Verificar firewall: `ufw status`
4. Verificar se porta está aberta: `netstat -tlnp | grep 7860`

### Erro: "API not initialized"
- A API precisa estar rodando antes da interface web
- Verificar logs da API: `tail -50 /var/log/npllm_api.log`

## 📊 Recursos

### Uso de Memória Esperado
- API: ~2-3GB (com modelo TinyLlama)
- Interface Web: ~50-100MB
- PostgreSQL: ~200MB
- **Total**: ~2.5-3.5GB

### Portas
- **8000**: API FastAPI
- **7860**: Interface Web Gradio
- **5433**: PostgreSQL (local) / 5432 (Docker)

## 🔄 Reiniciar Serviços

```bash
# Parar tudo
pkill -f src.api.server
pkill -f src.web

# Iniciar API
./deploy/start_api.sh

# Aguardar API inicializar (10-30s)
sleep 15

# Iniciar Interface Web
./deploy/start_web.sh 7860 http://localhost:8000
```

## 📝 Notas

- A interface web **não bloqueia** a API
- Pode rodar em **máquina diferente** da API (ajustar `--api-url`)
- Suporta **múltiplos usuários** simultâneos
- Interface é **leve** (~50MB RAM)

