# Spiking Neural Networks (SNNs) e Neuroplasticidade

## Introdução

Spiking Neural Networks (SNNs) são redes neurais que processam informações através de "spikes" (pulsos) discretos, imitando mais de perto o funcionamento de neurônios biológicos. São fundamentais para entender como implementar neuroplasticidade de forma mais biológica.

## Fundamentos Teóricos

### Conceito de Spiking

**Spikes**: Eventos discretos no tempo que representam atividade neural
- **Temporal Coding**: Informação codificada no timing dos spikes
- **Rate Coding**: Informação codificada na frequência de spikes
- **Population Coding**: Informação codificada em populações de neurônios

### Vantagens sobre Redes Tradicionais

1. **Eficiência Energética**: Processamento esparso, menos computação
2. **Processamento Temporal**: Naturalmente processa sequências temporais
3. **Biologicamente Plausível**: Mais próximo do cérebro biológico
4. **Event-Driven**: Computação apenas quando necessário

## Técnicas e Métodos

### 1. Spike-Timing Dependent Plasticity (STDP)

**Conceito**: Plasticidade baseada no timing relativo de spikes

**Regra**:
- Se pré-sináptico dispara antes do pós: **LTP** (fortalecimento)
- Se pós-sináptico dispara antes do pré: **LTD** (enfraquecimento)
- Janela temporal crítica (tipicamente 20-100ms)

**Implementação**:
```python
# Pseudocódigo STDP
if t_pre < t_post:  # Pré antes do pós
    weight += A_plus * exp(-(t_post - t_pre) / tau_plus)  # LTP
else:  # Pós antes do pré
    weight -= A_minus * exp(-(t_pre - t_post) / tau_minus)  # LTD
```

### 2. Triplet STDP

**Conceito**: Extensão do STDP que considera três spikes

**Vantagens**:
- Mais estável que STDP simples
- Melhor para aprendizado de padrões complexos

### 3. Voltage-Dependent Plasticity

**Conceito**: Plasticidade baseada no potencial de membrana

**Mecanismo**:
- Depende do estado do neurônio (subthreshold, spiking)
- Mais biologicamente plausível

### 4. Arquiteturas de SNNs

#### Leaky Integrate-and-Fire (LIF)

**Modelo**: Neurônio que integra inputs e dispara quando threshold é atingido

**Equações**:
- **Membrane Potential**: τ_m * dV/dt = -V + R*I
- **Spike**: V > V_threshold → spike, V = V_reset

**Características**:
- Simples e eficiente
- Boa aproximação de neurônios biológicos
- Amplamente usado

#### Izhikevich Model

**Conceito**: Modelo mais complexo que captura mais comportamentos

**Vantagens**:
- Mais comportamentos neuronais
- Ainda computacionalmente eficiente

#### Hodgkin-Huxley

**Conceito**: Modelo mais detalhado, fisiologicamente preciso

**Limitações**:
- Computacionalmente caro
- Menos usado em aplicações práticas

### 5. Aprendizado em SNNs

#### STDP Não-Supervisionado

**Conceito**: Aprendizado baseado apenas em STDP

**Aplicações**:
- Feature learning
- Clustering
- Pattern recognition

#### Backpropagation Through Time (BPTT)

**Conceito**: Adaptação de backpropagation para SNNs

**Desafios**:
- Spikes são não-diferenciáveis
- Requer aproximações (surrogate gradients)

#### Conversion from ANNs

**Conceito**: Converter redes neurais tradicionais para SNNs

**Métodos**:
- **Rate-based**: Ativações → firing rates
- **Spike-based**: Ativações → spike trains

**Vantagens**:
- Aproveita modelos pré-treinados
- Mais fácil de implementar

## Papers Relevantes

### Papers Fundamentais

1. **Spike-timing-dependent plasticity: from synapse to perception**
   - Dan, Y., & Poo, M. M. (2006)
   - Annual Review of Neuroscience
   - **Contribuição**: Base teórica do STDP

2. **Unsupervised learning of digit recognition using spike-timing-dependent plasticity**
   - Diehl, P. U., & Cook, M. (2015)
   - Frontiers in Computational Neuroscience
   - **Contribuição**: Aplicação prática de STDP

3. **Surrogate Gradient Learning in Spiking Neural Networks**
   - Neftci, E. O., et al. (2019)
   - Nature Machine Intelligence
   - **Contribuição**: Treinamento diferenciável de SNNs

## Implementações Práticas

### Frameworks

1. **PyTorch**: Suporte para SNNs via bibliotecas
2. **TensorFlow**: Implementações de SNNs
3. **Nengo**: Framework especializado em SNNs
4. **Brian**: Simulador de SNNs

### Repositórios

- **SpyTorch**: PyTorch para SNNs
- **snnTorch**: Biblioteca PyTorch
- **Nengo**: Framework oficial

### Hardware Neuromórfico

**Chips Especializados**:
1. **IBM TrueNorth**: Chip neuromórfico da IBM
2. **Intel Loihi**: Chip neuromórfico da Intel
3. **SpiNNaker**: Sistema neuromórfico da Manchester
4. **BrainScaleS**: Sistema neuromórfico europeu

**Vantagens**:
- Eficiência energética
- Processamento paralelo massivo
- Suporte nativo a spikes

## Casos de Uso

### 1. Continual Learning

**Aplicação**:
- STDP naturalmente suporta aprendizado contínuo
- Plasticidade local facilita preservação
- Ainda sofre com catastrophic forgetting

### 2. Memória de Trabalho

**Aplicação**:
- SNNs naturalmente mantêm estado temporal
- Útil para memória de curto prazo
- Processamento temporal nativo

### 3. Processamento Temporal

**Aplicação**:
- Naturalmente processa sequências
- Timing é fundamental
- Aplicações em processamento de sinais

## Limitações e Desafios

### Desafios Técnicos

1. **Treinamento**: Mais difícil que redes tradicionais
2. **Escalabilidade**: Ainda limitado em escala
3. **Hardware**: Requer hardware especializado para eficiência
4. **Integração**: Difícil integrar com LLMs tradicionais

### Limitações Atuais

- Ainda não aplicado extensivamente em LLMs
- Maioria das aplicações em visão computacional
- Requer expertise especializada
- Hardware neuromórfico ainda caro/limitado

## Direções Futuras

1. **SNNs para NLP**: Aplicação em processamento de linguagem
2. **Hybrid Models**: Combinação de SNNs e ANNs
3. **Hardware Acessível**: Chips neuromórficos mais baratos
4. **Better Training**: Métodos de treinamento mais eficientes

## Referências

### Papers Acadêmicos
- Dan, Y., & Poo, M. M. (2006). Spike-timing-dependent plasticity: from synapse to perception. Annual Review of Neuroscience
- Diehl, P. U., & Cook, M. (2015). Unsupervised learning of digit recognition using spike-timing-dependent plasticity. Frontiers in Computational Neuroscience
- Neftci, E. O., et al. (2019). Surrogate Gradient Learning in Spiking Neural Networks. Nature Machine Intelligence

### Recursos Online
- SpiNNaker: https://apt.cs.manchester.ac.uk/projects/SpiNNaker/
- Intel Loihi: https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html
- Papers with Code: Spiking Neural Networks
- GitHub: Repositórios de implementações open-source
