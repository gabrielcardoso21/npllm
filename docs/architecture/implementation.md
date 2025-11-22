# Implementação npllm - Documentação Técnica

## Visão Geral da Implementação

Este documento descreve a implementação técnica do NeuroPlastic Large Language Model (npllm), incluindo todas as decisões arquiteturais otimizadas para viabilidade em servidores com recursos limitados.

## Decisões Arquiteturais Implementadas

### 1. Modelo Base
- **CodeLlama 3B quantizado 4-bit (GGML)**
- Lazy loading para reduzir uso inicial de memória
- Cache de respostas frequentes
- Implementado em: `src/models/base_model.py`

### 2. Sistema de Adapters
- **LoRA adapters com versionamento simplificado (stable/experimental)**
- Lazy loading de adapters
- Gerenciamento eficiente de múltiplos adapters
- Implementado em: `src/adapters/`

### 3. Modulador
- **Modelo pequeno (1-5M parâmetros)**
- Bottom-up + top-down (inspirado em córtex pré-frontal)
- Seleção e modulação de adapters
- Implementado em: `src/models/modulador.py`

### 4. RAG (Otimizado: Sob Demanda)
- **PostgreSQL + pgvector**
- Busca apenas quando contexto não é suficiente
- Chunking semântico por função/classe
- Implementado em: `src/rag/`

### 5. Detecção de Contexto (Otimizado)
- **Apenas metadados + confirmação do usuário**
- Sem análise AST (reduz processamento)
- Implementado em: `src/context/`

### 6. Sistema de Feedback (Otimizado)
- **Implícito + Emocional**
- Sem feedback explícito (reduz complexidade)
- Implementado em: `src/feedback/`

### 7. Aprendizado Contínuo
- **MAS (Memory Aware Synapses) + Replay**
- Consolidação periódica após cada projeto
- Implementado em: `src/learning/`

### 8. Pipeline
- **Síncrono (crítico) + Assíncrono (aprendizado)**
- Cache inteligente
- Implementado em: `src/pipeline/`

### 9. Métricas (Otimizado)
- **Comportamento + Aprendizado**
- Sem métricas de qualidade e emocionais (reduz overhead)
- Implementado em: `src/metrics/`

## Estrutura de Arquivos

```
src/
├── models/          # Modelos LLM
├── adapters/        # Adapters LoRA
├── rag/             # Sistema RAG
├── learning/        # Aprendizado contínuo
├── feedback/        # Sistema de feedback
├── context/         # Detecção de contexto
├── data_collection/ # Coleta de dados
├── pipeline/         # Pipelines
├── metrics/         # Métricas
└── utils/           # Utilitários
```

## Uso de Recursos (Otimizado)

- **Memória Total**: ~6.6GB (viável com margem)
- **CPU Total**: ~3.4 vCPU (funciona bem)
- **Otimizações**: RAG sob demanda, detecção apenas metadados, versionamento simplificado

## Como Usar

```bash
# Desenvolvimento
python -m src.main --query "Como criar um modelo Odoo?"

# Produção
python -m src.main --config config/production.yaml
```

## Próximos Passos

1. Testes de viabilidade em servidores Contabo
2. Ajustes de otimização baseados em testes
3. Documentação de API
4. Guias de uso

