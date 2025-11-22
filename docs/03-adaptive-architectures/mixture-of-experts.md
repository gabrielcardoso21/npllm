# Mixture of Experts (MoE)

## Introdução

Mixture of Experts (MoE) é uma arquitetura onde múltiplos "especialistas" (sub-redes) são combinados com um mecanismo de roteamento adaptativo. Cada especialista processa diferentes tipos de inputs, permitindo modelos grandes com computação eficiente - similar à especialização no cérebro.

## Fundamentos Teóricos

### Conceito

**Componentes**:
1. **Experts**: Múltiplas sub-redes especializadas
2. **Router/Gating Network**: Decide qual expert usar
3. **Combination**: Combina outputs dos experts

**Vantagens**:
- Modelos grandes com menos computação
- Especialização automática
- Escalabilidade eficiente

## Técnicas e Métodos

### 1. Sparse MoE

**Paper**: "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer" (Shazeer et al., 2017)
- **ArXiv**: [1701.06538](https://arxiv.org/abs/1701.06538)

**Conceito**: Apenas alguns experts ativos por input

**Mecanismo**:
- Router seleciona top-k experts
- Apenas experts selecionados são computados
- Reduz computação drasticamente

**Vantagens**:
- Muito eficiente
- Escalável
- Especialização automática

### 2. Switch Transformers

**Paper**: "Switch Transformers: Scaling to Trillion Parameter Models" (Fedus et al., 2021)
- **ArXiv**: [2101.03961](https://arxiv.org/abs/2101.03961)
- **Google Research**

**Conceito**: MoE aplicado a Transformers

**Características**:
- Top-1 routing (apenas 1 expert)
- Simplifica roteamento
- Escala para trilhões de parâmetros

**Resultados**:
- Modelos com 1.6T parâmetros
- 7x mais rápido que modelos densos
- Boa performance

### 3. GShard

**Paper**: "GShard: Scaling Giant Models with Conditional Computation" (Lepikhin et al., 2020)
- **Google Research**

**Conceito**: MoE com sharding eficiente

**Características**:
- Sharding de experts em múltiplos devices
- Top-2 routing
- Escalabilidade massiva

### 4. GLaM (Generalist Language Model)

**Paper**: "GLaM: Efficient Scaling of Language Models with Mixture-of-Experts" (Du et al., 2021)
- **Google Research**

**Conceito**: MoE para LLMs gerais

**Características**:
- 1.2T parâmetros
- 2 experts ativos por token
- Performance competitiva com GPT-3

### 5. Expert Choice Routing

**Paper**: "Expert Choice Routing" (Zhou et al., 2022)

**Conceito**: Routing melhorado, experts escolhem tokens

**Mecanismo**:
- Inverte routing: experts escolhem tokens
- Melhor balanceamento de carga
- Mais estável

## Papers Relevantes

### Fundamentais

1. **Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer**
   - Shazeer, N., et al. (2017)
   - ArXiv: [1701.06538](https://arxiv.org/abs/1701.06538)
   - **Contribuição**: MoE esparso escalável

2. **Switch Transformers: Scaling to Trillion Parameter Models**
   - Fedus, W., Zoph, B., & Shazeer, N. (2021)
   - ArXiv: [2101.03961](https://arxiv.org/abs/2101.03961)
   - **Contribuição**: MoE em Transformers, trilhões de parâmetros

3. **GShard: Scaling Giant Models with Conditional Computation**
   - Lepikhin, D., et al. (2020)
   - ArXiv: [2006.16668](https://arxiv.org/abs/2006.16668)
   - **Contribuição**: Sharding eficiente

4. **GLaM: Efficient Scaling of Language Models**
   - Du, N., et al. (2021)
   - ArXiv: [2112.06905](https://arxiv.org/abs/2112.06905)
   - **Contribuição**: MoE para LLMs gerais

### Avanços Recentes

5. **ST-MoE: Designing Stable and Transferable Sparse Expert Models**
   - Zoph, B., et al. (2022)
   - ArXiv: [2202.08906](https://arxiv.org/abs/2202.08906)
   - **Contribuição**: MoE estável e transferível

## Implementações Práticas

### Frameworks

1. **Mesh TensorFlow**: Framework do Google para MoE
2. **JAX/Flax**: Implementações em JAX
3. **PyTorch**: Implementações customizadas
4. **Hugging Face**: Modelos MoE (Switch, etc.)

### Repositórios

- **Switch Transformers**: Código oficial Google
- **GShard**: Implementação Google
- **Hugging Face**: Modelos pré-treinados

## Casos de Uso

### 1. Modelos Gigantes Eficientes
- Modelos com trilhões de parâmetros
- Computação eficiente

### 2. Especialização Automática
- Experts especializam-se automaticamente
- Adaptação a diferentes tipos de inputs

### 3. Escalabilidade
- Escala para modelos muito grandes
- Distribuição eficiente

### 4. Multi-Domain Models
- Modelos que funcionam em múltiplos domínios
- Especialização por domínio

## Limitações e Desafios

### Desafios Técnicos

1. **Load Balancing**: Balancear carga entre experts
2. **Routing Learning**: Aprender roteamento eficiente
3. **Communication**: Comunicação entre experts
4. **Training Stability**: Estabilidade no treinamento

### Limitações Atuais

- Requer infraestrutura especializada
- Routing pode ser instável
- Load balancing desafiador
- Ainda experimental em muitos casos

## Direções Futuras

1. **MoE Mais Eficiente**: Redução de overhead
2. **Better Routing**: Roteamento mais inteligente
3. **Hardware Support**: Suporte de hardware especializado
4. **MoE em Mais Domínios**: Aplicação expandida

## Referências

### Papers Acadêmicos
- Shazeer, N., et al. (2017). MoE. ArXiv:1701.06538
- Fedus, W., et al. (2021). Switch Transformers. ArXiv:2101.03961
- Lepikhin, D., et al. (2020). GShard. ArXiv:2006.16668
- Du, N., et al. (2021). GLaM. ArXiv:2112.06905

### Recursos
- Hugging Face: Modelos MoE
- Papers with Code: Mixture of Experts
- GitHub: Implementações open-source
