# NeuroPlastic Large Language Model (npllm)

Sistema de assistente de código geral que aprende padrões arquiteturais e aplica conhecimento entre projetos.

## 🎯 Objetivo

Criar um assistente de código que:
- **Aprende padrões arquiteturais** de qualquer projeto
- **Aprende em um projeto e aplica em outro** (transfer learning)
- **Foca em arquitetura e engenharia**, não código de baixo nível
- **Aprende continuamente** e melhora com o tempo
- **Processa feedback emocional** para guiar aprendizado

**Filosofia**: O futuro é de quem sabe arquitetar e gerenciar IA, não de quem escreve código de baixo/médio nível.

## 🏗️ Arquitetura Simplificada

O sistema foi simplificado significativamente, mantendo apenas 6 componentes essenciais:

1. **LLM Base (CodeLlama 3B)** - Não treina (plug-and-play)
2. **Seletor de Adapter** - Seleção direta por contexto
3. **LoRA Adapters** - Treina apenas durante sono
4. **PostgreSQL + pgvector** - Armazenamento
5. **Análise Emocional (RoBERTa)** - Captura emoção
6. **Sistema de Sono** - Consolidação durante inatividade

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 14+ com extensão pgvector (ou Docker)
- 4 vCPU + 8GB RAM (mínimo)
- Linux (testado em Ubuntu 22.04)

## 🚀 Instalação Rápida

### 1. Clone o repositório

```bash
git clone https://github.com/gabrielcardoso21/npllm.git
cd npllm
```

### 2. Configure ambiente

```bash
# Crie ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 3. Configure PostgreSQL (Docker)

```bash
# Copie configuração
cp .env.docker .env

# Inicie PostgreSQL
./INICIAR_DOCKER.sh
```

### 4. Execute teste

```bash
./EXECUTAR_TESTE_REAL.sh
```

## 📚 Documentação

### Essencial
- **[Arquitetura Final](docs/mvp-general-assistant/ARQUITETURA-FINAL.md)** - Arquitetura completa com diagramas
- **[Plano de Implementação](docs/mvp-general-assistant/IMPLEMENTACAO-MVP.md)** - Plano detalhado de implementação

### Setup
- **[Docker Quick Start](DOCKER_QUICKSTART.md)** - Setup rápido com Docker
- **[Setup Docker](SETUP_DOCKER.md)** - Setup detalhado
- **[Setup Teste Real](SETUP_TESTE_REAL.md)** - Setup para testes
- **[Recursos](RECURSOS_RESUMO.md)** - Análise de recursos necessários

## 🧪 Testes

```bash
# Todos os testes
pytest

# Testes de integração
pytest tests/integration/

# Com cobertura
pytest --cov=src --cov-report=html
```

**Status**: 72 testes passando (96% de sucesso)

## 📁 Estrutura do Projeto

```
npllm/
├── src/                    # Código fonte
│   ├── models/            # LLM Base
│   ├── adapters/          # LoRA Adapters + Seletor
│   ├── storage/           # PostgreSQL
│   ├── feedback/          # Análise Emocional + Implícito
│   ├── learning/          # Sono + Replay + Fine-tuning
│   ├── analysis/          # Análise Arquitetural
│   ├── transfer/          # Transfer Learning
│   ├── generation/        # Geração Arquitetural
│   └── utils/             # Utilitários
├── tests/                  # Testes
├── docs/                   # Documentação
│   └── mvp-general-assistant/  # Arquitetura final
├── docker-compose.yml      # PostgreSQL
└── requirements.txt        # Dependências
```

## 🔧 Uso

### Linha de Comando

```bash
# Processar query
python -m src.main --query "Create a hello function" --project-path /path/to/project

# Analisar projeto
python -m src.main --analyze /path/to/project

# Acionar sono manualmente
python -m src.main --sleep
```

### Python

```python
from src.main import NpllmSystem

# Inicializa sistema
system = NpllmSystem()

# Processa query
result = system.process_query(
    query="Create a hello function in Python",
    file_path="test.py"
)

# Captura feedback
system.capture_feedback(
    query="Create a hello function in Python",
    response=result["response"],
    user_reaction="Perfect!",
    user_action=UserAction.ACCEPT
)

# Fecha sistema
system.close()
```

## 📊 Status

- ✅ Arquitetura definida
- ✅ Implementação completa
- ✅ 72 testes passando
- ✅ Docker configurado
- ⏳ Testes em ambiente real

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Leia a [Arquitetura Final](docs/mvp-general-assistant/ARQUITETURA-FINAL.md)
2. Siga o [Plano de Implementação](docs/mvp-general-assistant/IMPLEMENTACAO-MVP.md)
3. Execute os testes antes de fazer PR

## 📄 Licença

MIT
