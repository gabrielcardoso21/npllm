# Guia de Início Rápido

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/gabrielcardoso21/npllm.git
cd npllm
```

2. Configure ambiente:
```bash
bash deployment/scripts/setup_environment.sh
source venv/bin/activate
```

3. Configure PostgreSQL:
```bash
bash deployment/scripts/setup_postgres.sh
```

4. Configure variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

## Uso Básico

### Processar uma query:
```bash
python -m src.main --query "Como criar um modelo Odoo?" --project-path /path/to/project
```

### Modo interativo:
```bash
python -m src.main
```

## Configuração

Edite `config/default.yaml` para ajustar configurações:
- Modelo base
- Configurações de RAG
- Configurações de adapters
- Limites de recursos

## Próximos Passos

- Veja `docs/api/README.md` para documentação de API
- Veja `docs/architecture/implementation.md` para detalhes técnicos

