# NeuroPlastic Large Language Model (npllm)

Sistema de assistente de programação com neuroplasticidade que aprende continuamente do código do usuário, aplicando conhecimento aprendido em novos projetos.

## Características Principais

- **Neuroplasticidade**: Aprende continuamente sem esquecer conhecimento anterior
- **Arquitetura Híbrida**: Modelo grande estático + adapters dinâmicos + modulador
- **Otimizado para Recursos Limitados**: Funciona em servidores com 4 vCPU + 8GB RAM
- **RAG Sob Demanda**: Busca contexto apenas quando necessário
- **Feedback Emocional**: Analisa sentimento do usuário para melhorar aprendizado

## Arquitetura

- **Modelo Base**: CodeLlama 3B quantizado 4-bit (GGML)
- **Adapters**: LoRA adapters para diferentes contextos
- **Modulador**: Modelo pequeno (1-5M) que escolhe e modula adapters
- **Memória**: PostgreSQL + pgvector para RAG
- **Aprendizado**: MAS (Memory Aware Synapses) + Replay

## Requisitos

- Python 3.10+
- PostgreSQL 14+ com extensão pgvector
- 4 vCPU + 8GB RAM (mínimo)
- Linux (testado em Ubuntu 22.04)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/gabrielcardoso21/npllm.git
cd npllm

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure PostgreSQL + pgvector
# Veja deployment/scripts/setup_postgres.sh

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações
```

## Uso

```bash
# Desenvolvimento
python -m src.main

# Produção
python -m src.main --config config/production.yaml
```

## Estrutura do Projeto

```
npllm/
├── src/              # Código fonte
├── tests/            # Testes
├── deployment/       # Scripts de deploy
├── docs/             # Documentação
└── config/           # Configurações
```

## Documentação

Veja `docs/` para documentação completa sobre:
- Arquitetura e decisões de design
- Guias de implementação
- Casos de uso
- Otimizações

## Licença

MIT

## Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

