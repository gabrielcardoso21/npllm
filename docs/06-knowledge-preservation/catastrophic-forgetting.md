# Catastrophic Forgetting (Esquecimento Catastrófico)

## Introdução

Catastrophic forgetting é o fenômeno onde modelos de deep learning esquecem drasticamente conhecimento anterior ao aprender novas informações. É um dos maiores desafios para neuroplasticidade em LLMs.

## Fundamentos Teóricos

### Definição

**Catastrophic Forgetting**: Perda rápida e severa de performance em tarefas anteriores quando modelo aprende nova tarefa

**Causas**:
- **Parameter Overwriting**: Novos dados sobrescrevem parâmetros importantes
- **Distribution Shift**: Mudança na distribuição de dados
- **Local Optimization**: Otimização local vs. global
- **Lack of Rehearsal**: Não revisar dados antigos

### Por que Acontece

1. **Gradient Descent**: Otimiza para nova tarefa, ignora antiga
2. **Shared Representations**: Representações compartilhadas são modificadas
3. **No Memory**: Modelos não têm memória explícita de tarefas antigas

## Técnicas de Mitigação

### 1. Elastic Weight Consolidation (EWC)

**Paper**: "Overcoming catastrophic forgetting in neural networks" (Kirkpatrick et al., 2017)

**Mecanismo**:
- Calcula importância de parâmetros (Fisher Information)
- Adiciona penalidade para mudanças em parâmetros importantes
- Permite adaptação de parâmetros menos importantes

**Vantagens**:
- Não requer dados antigos
- Relativamente simples
- Eficaz para poucas tarefas

**Limitações**:
- Cálculo de Fisher é caro
- Não escala bem
- Pode ser muito conservador

### 2. Memory Aware Synapses (MAS)

**Paper**: "Memory Aware Synapses: Learning what (not) to forget" (Aljundi et al., 2017)

**Mecanismo**:
- Calcula importância baseada em gradientes
- Não requer dados de validação
- Aprendizado não-supervisionado

**Vantagens**:
- Não requer labels
- Computacionalmente eficiente
- Adaptativo

### 3. Progressive Neural Networks

**Paper**: "Progressive Neural Networks" (Rusu et al., 2016)

**Mecanismo**:
- Adiciona nova coluna para cada tarefa
- Colunas anteriores congeladas
- Conexões laterais para transferência

**Vantagens**:
- Zero esquecimento garantido
- Transfer learning explícito

**Limitações**:
- Crescimento linear de parâmetros
- Não eficiente para muitas tarefas

### 4. Replay Mechanisms

**Conceito**: Reapresentar dados de tarefas anteriores

**Tipos**:
- **Experience Replay**: Armazenar e reutilizar exemplos
- **Generative Replay**: Gerar exemplos sintéticos
- **Pseudo-Rehearsal**: Gerar exemplos de modelo antigo

**Vantagens**:
- Muito eficaz
- Simples de entender

**Limitações**:
- Requer armazenamento
- Pode ser computacionalmente caro

### 5. Regularization Methods

**Tipos**:
- **L2 Regularization**: Penalizar mudanças grandes
- **Dropout**: Regularização durante treinamento
- **Weight Constraints**: Limitar mudanças de pesos

**Eficácia**: Limitada, mas simples

## Papers Relevantes

### Fundamentais

1. **Overcoming catastrophic forgetting in neural networks**
   - Kirkpatrick, J., et al. (2017)
   - PNAS, 114(13), 3521-3526
   - **Contribuição**: EWC, base para muitos métodos

2. **Memory Aware Synapses: Learning what (not) to forget**
   - Aljundi, R., et al. (2017)
   - ArXiv: [1711.09601](https://arxiv.org/abs/1711.09601)
   - **Contribuição**: MAS, importância não-supervisionada

3. **Progressive Neural Networks**
   - Rusu, A. A., et al. (2016)
   - ArXiv: [1606.04671](https://arxiv.org/abs/1606.04671)
   - **Contribuição**: Crescimento sem esquecimento

### Surveys

4. **Continual Lifelong Learning with Neural Networks: A Review**
   - Parisi, G. I., et al. (2019)
   - Neural Networks, 113, 54-71
   - **Contribuição**: Survey abrangente

## Implementações Práticas

### Frameworks

1. **Avalanche**: Framework com implementações
2. **Continuum**: Framework para continual learning
3. **PyTorch**: Implementações customizadas

### Repositórios

- **EWC, MAS**: Implementações diversas
- **Progressive Networks**: Código disponível
- **Papers with Code**: Continual Learning section

## Casos de Uso

### 1. Fine-tuning Sem Degradação
- Fine-tuning sem perder performance em tarefas antigas
- Adaptação a novos domínios

### 2. Aprendizado Sequencial
- Aprender múltiplas tarefas sequencialmente
- Preservar conhecimento

### 3. Personalização
- Adaptar a usuários sem perder capacidade geral
- Balancear personalização e generalização

## Limitações e Desafios

### Desafios Técnicos

1. **Escalabilidade**: Métodos não escalam bem
2. **Balanceamento**: Preservação vs. adaptação
3. **Eficiência**: Overhead computacional
4. **Generalização**: Métodos podem não generalizar

### Limitações Atuais

- Maioria testada em poucas tarefas
- Não aplicado extensivamente em LLMs grandes
- Ainda ocorre em muitos casos
- Requer trade-offs

## Direções Futuras

1. **Métodos Escaláveis**: Escalar para modelos grandes
2. **Better Balance**: Melhor balanceamento
3. **Efficient Methods**: Redução de overhead
4. **Theoretical Understanding**: Melhor compreensão teórica

## Referências

### Papers Acadêmicos
- Kirkpatrick, J., et al. (2017). Overcoming catastrophic forgetting. PNAS
- Aljundi, R., et al. (2017). Memory Aware Synapses. ArXiv:1711.09601
- Rusu, A. A., et al. (2016). Progressive Neural Networks. ArXiv:1606.04671
- Parisi, G. I., et al. (2019). Continual Learning Review. Neural Networks

### Recursos
- Avalanche: https://avalanche.continualai.org
- Papers with Code: Continual Learning
- GitHub: Implementações open-source
