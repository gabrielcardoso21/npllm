# Scripts de Deploy

Scripts para fazer deploy do npllm no Contabo.

## Arquivos

- **`deploy.sh`**: Script principal de deploy (executa na sua máquina)
- **`setup_production.sh`**: Setup de produção (executa no servidor)
- **`DEPLOY_CONTABO.md`**: Documentação completa de deploy

## Uso Rápido

```bash
# Na sua máquina
./deploy/deploy.sh [IP_SERVIDOR] [USUARIO]

# Exemplo
./deploy/deploy.sh 161.97.123.192 root
```

Depois, no servidor:
```bash
cd /opt/npllm
./deploy/setup_production.sh
```

Veja `DEPLOY_CONTABO.md` para documentação completa.

