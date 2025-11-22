# Benchmarks e Métricas para Neuroplasticidade

## Introdução

Este documento apresenta métricas e benchmarks para avaliar neuroplasticidade em LLMs, incluindo como medir retenção de conhecimento, adaptação e performance geral.

## Métricas Principais

### 1. Retenção de Conhecimento

**Métrica**: **Backward Transfer (BWT)**

```
BWT = (1/(T-1)) * Σ(R_{T,i} - R_{i,i})
```

Onde:
- `R_{T,i}`: Performance na tarefa i após aprender T tarefas
- `R_{i,i}`: Performance na tarefa i quando aprendida

**Interpretação**:
- **BWT > 0**: Melhora (positive transfer)
- **BWT = 0**: Sem mudança
- **BWT < 0**: Esquecimento (catastrophic forgetting)

### 2. Adaptação

**Métrica**: **Forward Transfer (FWT)**

```
FWT = (1/(T-1)) * Σ(R_{i,i} - R_{0,i})
```

Onde:
- `R_{0,i}`: Performance baseline na tarefa i

**Interpretação**: Quanto conhecimento anterior ajuda em novas tarefas

### 3. Performance Geral

**Métrica**: **Average Accuracy (ACC)**

```
ACC = (1/T) * Σ R_{T,i}
```

**Interpretação**: Performance média em todas as tarefas após aprender todas

## Benchmarks Padronizados

### 1. CLIP (Continual Learning in Practice)

**Foco**: Continual learning em visão

**Tarefas**: Múltiplos datasets de classificação

**Métricas**: ACC, BWT, FWT

### 2. CORe50

**Foco**: Continual learning em objetos

**Características**: 50 objetos, 10 sessões

### 3. Split-CIFAR

**Foco**: Continual learning em CIFAR

**Tarefas**: CIFAR-10/100 dividido em tarefas

### 4. Permuted MNIST

**Foco**: Continual learning simples

**Tarefas**: MNIST com permutações diferentes

## Métricas Específicas para LLMs

### 1. Perplexity Retention

**Métrica**: Manutenção de perplexity em tarefas antigas

```
Retention = PPL_old / PPL_original
```

### 2. Task Accuracy Retention

**Métrica**: Manutenção de accuracy em tarefas antigas

```
Retention = ACC_after / ACC_before
```

### 3. Adaptation Speed

**Métrica**: Velocidade de adaptação a nova tarefa

```
Speed = 1 / epochs_to_convergence
```

## Datasets Recomendados

### Para NLP Continual Learning

1. **GLUE**: Múltiplas tarefas de NLP
2. **SuperGLUE**: Tarefas mais desafiadoras
3. **SQuAD**: Question answering
4. **MultiNLI**: Natural language inference

### Para Domain Adaptation

1. **Amazon Reviews**: Múltiplos domínios
2. **News Classification**: Diferentes fontes
3. **Medical/Legal Text**: Domínios especializados

## Implementação de Avaliação

### Exemplo: Avaliar EWC

```python
from avalanche.evaluation import MetricTracker
from avalanche.training import EWC

# Criar tracker
metrics = MetricTracker()

# Treinar e avaliar
for experience in benchmark.train_stream:
    strategy.train(experience)
    metrics.update(strategy, experience)
    
# Calcular métricas
acc = metrics.get_last_metric_value('Top1_Acc')
bwt = calculate_backward_transfer(metrics)
```

## Referências

- Avalanche Benchmarks: https://avalanche.continualai.org/benchmarks
- Papers with Code: Continual Learning Benchmarks
- CLIP Benchmark: https://github.com/ContinualAI/CLIP-Benchmark

