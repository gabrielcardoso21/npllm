# 🐳 Docker Quick Start

**Data**: 2025-01-27

---

## ⚡ Início Rápido (3 comandos)

```bash
# 1. Configurar ambiente
cp .env.docker .env

# 2. Iniciar PostgreSQL
./INICIAR_DOCKER.sh

# 3. Executar teste
./EXECUTAR_TESTE_REAL.sh
```

**Pronto!** 🎉

---

## 📋 O Que Foi Configurado

### ✅ Docker Compose

- **PostgreSQL 16** com **pgvector** pré-instalado
- **Porta**: 5432 (localhost)
- **Banco**: npllm
- **Usuário**: npllm_user
- **Senha**: npllm_password

### ✅ Scripts Automáticos

- `INICIAR_DOCKER.sh` - Inicia e configura tudo
- `EXECUTAR_TESTE_REAL.sh` - Detecta Docker automaticamente

---

## 🎯 Vantagens

✅ **Sem instalação local** - Tudo no Docker  
✅ **Fácil remoção** - `docker-compose down -v`  
✅ **Isolado** - Não polui sistema  
✅ **Pré-configurado** - pgvector já habilitado  
✅ **Portátil** - Funciona em qualquer máquina  

---

## 🛠️ Comandos Úteis

```bash
# Iniciar
./INICIAR_DOCKER.sh

# Ver logs
docker compose logs -f postgres

# Parar
docker compose stop

# Parar e remover (APAGA DADOS!)
docker compose down -v

# Status
docker compose ps
```

---

## ⚠️ Nota sobre Docker Compose

O script suporta ambos:
- **Docker Compose V2**: `docker compose` (recomendado)
- **Docker Compose V1**: `docker-compose` (legado)

Se tiver problemas, verifique:
```bash
docker compose version
# ou
docker-compose --version
```

---

**Última Atualização**: 2025-01-27

