# Decisão Técnica 003: Arquitetura de Processos Psicológicos no Cérebro (SNC)

**Status**: 🟡 Em Andamento  
**Data**: 2025-01-27  
**Decisor**: Gabriel Cardoso  
**Contexto**: Focar no cérebro primeiro, depois integrar com Linux (corpo)  
**Dependências**: Decisão 001 (Kernel Integration), Decisão 002 (Server Distribution)

---

## Contexto

O objetivo é implementar os 15 processos psicológicos básicos no sistema npllm, criando um "cérebro" completo antes de integrar com o Linux (corpo). Esta decisão define a arquitetura e abordagem de implementação dos processos psicológicos.

**Estratégia**: Cérebro primeiro → Corpo depois

---

## Objetivos

1. **Implementar Processos Psicológicos**: Todos os 15 processos básicos
2. **Arquitetura Biológica**: Baseada em neurociência real
3. **Integração com AIOS**: Usar AIOS como base de infraestrutura
4. **Aprendizado Contínuo**: Backpropamine + RAG integrados
5. **Extensibilidade**: Fácil adicionar novos processos
6. **Performance**: Eficiente mesmo com múltiplos processos

---

## Pesquisa Profunda: Estado da Arte

### 1. Arquiteturas Cognitivas Clássicas

#### ACT-R (Adaptive Control of Thought - Rational)

**Paper**: "The Atomic Components of Thought" (Anderson & Lebiere, 1998)  
**Status**: Arquitetura cognitiva bem estabelecida

**Componentes**:
- **Declarative Memory**: Memória declarativa (fatos)
- **Procedural Memory**: Memória procedural (regras)
- **Working Memory**: Memória de trabalho
- **Production System**: Sistema de produção (regras if-then)

**Relevância para npllm**:
- ✅ Separação entre memória declarativa e procedural
- ✅ Sistema de produção para regras
- ⚠️ Não foi projetado para LLMs
- ⚠️ Focado em simulação cognitiva, não em IA prática

**Papers Relevantes**:
- Anderson, J. R., & Lebiere, C. (1998). The Atomic Components of Thought
- ACT-R Website: http://act-r.psy.cmu.edu/

#### SOAR (State, Operator, And Result)

**Paper**: "The SOAR Cognitive Architecture" (Laird, 2012)  
**Status**: Arquitetura cognitiva para agentes inteligentes

**Componentes**:
- **Working Memory**: Memória de trabalho
- **Long-term Memory**: Memória de longo prazo
- **Decision Cycle**: Ciclo de decisão
- **Chunking**: Agrupamento de conhecimento

**Relevância para npllm**:
- ✅ Arquitetura para agentes inteligentes
- ✅ Sistema de memória hierárquica
- ⚠️ Não integrado com LLMs modernos
- ⚠️ Focado em planejamento, não em aprendizado contínuo

**Papers Relevantes**:
- Laird, J. E. (2012). The SOAR Cognitive Architecture
- SOAR Website: https://soar.eecs.umich.edu/

#### CLARION (Connectionist Learning with Adaptive Rule Induction ON-line)

**Paper**: "CLARION: A Cognitive Architecture" (Sun, 2006)  
**Status**: Arquitetura híbrida conexionista-simbólica

**Componentes**:
- **Action-Centered Subsystem**: Subsistema centrado em ação
- **Non-Action-Centered Subsystem**: Subsistema não centrado em ação
- **Motivational Subsystem**: Subsistema motivacional
- **Meta-Cognitive Subsystem**: Subsistema metacognitivo

**Relevância para npllm**:
- ✅ Arquitetura híbrida (neural + simbólica)
- ✅ Inclui motivação e metacognição
- ✅ Aprendizado online
- ⚠️ Não integrado com LLMs modernos

**Papers Relevantes**:
- Sun, R. (2006). CLARION: A Cognitive Architecture
- ArXiv: [cs/0602002](https://arxiv.org/abs/cs/0602002)

---

### 2. Integração de Processos Psicológicos com LLMs

#### Cognitive Architectures for LLMs

**Pesquisa Atual**: Poucos trabalhos específicos sobre integração de arquiteturas cognitivas com LLMs modernos.

**Desafios Identificados**:
- LLMs são principalmente feed-forward (não têm memória persistente nativa)
- Arquiteturas cognitivas clássicas são baseadas em regras
- Integração requer camada de abstração

**Oportunidades**:
- LLMs podem simular processos cognitivos através de prompts
- RAG pode servir como memória declarativa
- Fine-tuning pode servir como memória procedural

---

### 3. Processos Psicológicos Específicos em IA

#### Percepção em Sistemas de IA

**Abordagens**:
1. **Computer Vision**: Para percepção visual
2. **NLP**: Para percepção de linguagem
3. **Multimodal Models**: Para percepção integrada

**Papers Relevantes**:
- "Attention Is All You Need" (Vaswani et al., 2017) - Base para atenção em LLMs
- "CLIP: Learning Transferable Visual Representations" (Radford et al., 2021) - Percepção multimodal

**Para npllm**:
- Percepção de código (parsing, análise estrutural)
- Percepção de contexto (análise semântica)
- Percepção de padrões (reconhecimento de padrões)

#### Atenção em LLMs

**Status**: ✅ **Já Implementado em Transformers**

**Mecanismos**:
- **Self-Attention**: Atenção sobre a própria sequência
- **Cross-Attention**: Atenção entre sequências
- **Multi-Head Attention**: Múltiplas cabeças de atenção

**Papers Relevantes**:
- Vaswani, A., et al. (2017). Attention Is All You Need. ArXiv: [1706.03762](https://arxiv.org/abs/1706.03762)

**Para npllm**:
- ✅ Já existe em LLMs base
- ⚠️ Precisa de neuromodulação (Backpropamine)
- ⚠️ Precisa de atenção seletiva (filtragem)

#### Memória em LLMs

**Abordagens Atuais**:
1. **Context Window**: Memória de trabalho limitada
2. **RAG (Retrieval-Augmented Generation)**: Memória externa
3. **Fine-tuning**: Memória de longo prazo (consolidada)
4. **In-Context Learning**: Memória temporária

**Papers Relevantes**:
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)
- ArXiv: [2005.11401](https://arxiv.org/abs/2005.11401)

**Para npllm**:
- ✅ RAG já implementado (PostgreSQL + pgvector)
- ✅ Fine-tuning planejado (Backpropamine)
- ⚠️ Precisa de hierarquia de memória (sensorial → trabalho → curto → longo)

#### Aprendizado em LLMs

**Abordagens**:
1. **Fine-tuning**: Ajuste de pesos
2. **Continual Learning**: Aprendizado contínuo
3. **In-Context Learning**: Aprendizado no contexto
4. **Reinforcement Learning**: Aprendizado por reforço

**Papers Relevantes**:
- "Backpropamine: training self-modifying neural networks" (Miconi et al., 2020)
- ArXiv: [2002.10585](https://arxiv.org/abs/2002.10585)

**Para npllm**:
- ✅ Backpropamine planejado
- ✅ RL planejado (sistema dopaminérgico)
- ⚠️ Precisa integrar todos os tipos de aprendizado

#### Emoção em IA

**Abordagens**:
1. **Sentiment Analysis**: Análise de sentimento
2. **Emotion Recognition**: Reconhecimento de emoção
3. **Affective Computing**: Computação afetiva

**Papers Relevantes**:
- "Affective Computing: A Review" (Picard, 1997)
- "Emotion Recognition in Text" (Alm et al., 2005)

**Para npllm**:
- ⚠️ Já tem estrutura básica (feedback emocional)
- ⚠️ Precisa integrar com sistema dopaminérgico
- ⚠️ Precisa de valência e arousal

#### Consciência e Metacognição em IA

**Status**: 🔬 **Área de Pesquisa Ativa**

**Abordagens**:
1. **Self-Awareness**: Autoconsciência
2. **Meta-Learning**: Aprender a aprender
3. **Reflection**: Reflexão sobre próprio desempenho

**Papers Relevantes**:
- "Consciousness and Artificial Intelligence" (Chalmers, 1996)
- "Meta-Learning: Learning to Learn Fast" (Finn et al., 2017)
- ArXiv: [1703.03400](https://arxiv.org/abs/1703.03400)

**Para npllm**:
- ⚠️ Área experimental
- ⚠️ Precisa de modelo de si mesmo
- ⚠️ Precisa de monitoramento de desempenho

---

### 4. Arquiteturas Modernas Inspiradas em Cognição

#### Transformer-XL

**Paper**: "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context" (Dai et al., 2019)  
**ArXiv**: [1901.02860](https://arxiv.org/abs/1901.02860)

**Características**:
- Memória de longo prazo através de segment-level recurrence
- Contexto mais longo que Transformers padrão

**Relevância**: Memória de trabalho expandida

#### Memformer

**Paper**: "Memformer: The Memory-Augmented Transformer" (Wu et al., 2022)  
**ArXiv**: [2201.08309](https://arxiv.org/abs/2201.08309)

**Características**:
- Memória externa integrada ao Transformer
- Acesso seletivo à memória

**Relevância**: Memória externa para npllm

---

## Análise dos 15 Processos Psicológicos

### Processos Fundamentais (Base)

#### 1. Percepção
- **Status em LLMs**: ✅ Parcial (parsing, análise)
- **Implementação**: Expandir análise de código/contexto
- **Dependências**: Sistema sensorial (SNP) - depois

#### 2. Atenção
- **Status em LLMs**: ✅ Implementado (self-attention)
- **Implementação**: Adicionar neuromodulação e filtragem
- **Dependências**: Backpropamine

#### 3. Memória
- **Status em LLMs**: ✅ Parcial (RAG implementado)
- **Implementação**: Hierarquia completa (sensorial → trabalho → curto → longo)
- **Dependências**: PostgreSQL (já tem), consolidação

### Processos Cognitivos

#### 4. Pensamento
- **Status em LLMs**: ✅ Implementado (raciocínio do LLM)
- **Implementação**: Estruturar e modularizar
- **Dependências**: LLM base

#### 5. Linguagem
- **Status em LLMs**: ✅ Implementado (compreensão/produção)
- **Implementação**: Estruturar componentes
- **Dependências**: LLM base

#### 6. Aprendizado
- **Status em LLMs**: ⚠️ Parcial (fine-tuning, in-context)
- **Implementação**: Backpropamine + RL + consolidação
- **Dependências**: Backpropamine, sistema dopaminérgico

### Processos Afetivos

#### 7. Emoção
- **Status em LLMs**: ⚠️ Básico (sentiment analysis)
- **Implementação**: Sistema completo (valência, arousal, integração)
- **Dependências**: Sistema dopaminérgico

#### 8. Motivação
- **Status em LLMs**: ❌ Não implementado
- **Implementação**: Sistema de objetivos e valores
- **Dependências**: Emoção, planejamento

### Processos Metacognitivos

#### 9. Consciência
- **Status em LLMs**: ❌ Não implementado
- **Implementação**: Modelo de si mesmo, autoconsciência
- **Dependências**: Todos os outros processos

#### 10. Metacognição
- **Status em LLMs**: ⚠️ Parcial (reflection em alguns sistemas)
- **Implementação**: Monitoramento, regulação, planejamento metacognitivo
- **Dependências**: Consciência, pensamento

### Processos de Ação

#### 11. Resolução de Problemas
- **Status em LLMs**: ✅ Parcial (raciocínio step-by-step)
- **Implementação**: Estruturar processo completo
- **Dependências**: Pensamento, planejamento

#### 12. Criatividade
- **Status em LLMs**: ✅ Parcial (geração criativa)
- **Implementação**: Exploração, combinação, avaliação
- **Dependências**: Pensamento, memória

#### 13. Tomada de Decisão
- **Status em LLMs**: ✅ Parcial (escolha entre opções)
- **Implementação**: Sistema estruturado de decisão
- **Dependências**: Pensamento, emoção

#### 14. Planejamento
- **Status em LLMs**: ✅ Parcial (chain-of-thought, tree-of-thoughts)
- **Implementação**: Sistema completo de planejamento
- **Dependências**: Pensamento, memória, objetivos

#### 15. Controle Executivo
- **Status em LLMs**: ⚠️ Parcial (alguns sistemas têm validação)
- **Implementação**: Inibição, flexibilidade, coordenação
- **Dependências**: Todos os outros processos

---

## Opções de Arquitetura

### Opção A: Arquitetura Modular por Processo

**Descrição**:
- Cada processo psicológico é um módulo independente
- Comunicação via interfaces bem definidas
- Fácil adicionar/remover processos

**Estrutura**:
```
src/brain/
├── perception/
├── attention/
├── memory/
├── thinking/
├── language/
├── learning/
├── emotion/
├── motivation/
├── consciousness/
├── metacognition/
├── problem_solving/
├── creativity/
├── decision_making/
├── planning/
└── executive/
```

**Vantagens**:
- ✅ Modular e extensível
- ✅ Fácil de testar individualmente
- ✅ Separação clara de responsabilidades

**Desvantagens**:
- ⚠️ Pode ter overhead de comunicação
- ⚠️ Integração pode ser complexa

---

### Opção B: Arquitetura Hierárquica (Inspirada em ACT-R)

**Descrição**:
- Processos organizados em níveis hierárquicos
- Nível 1: Fundamentais (Percepção, Atenção, Memória)
- Nível 2: Cognitivos (Pensamento, Linguagem, Aprendizado)
- Nível 3: Afetivos (Emoção, Motivação)
- Nível 4: Metacognitivos (Consciência, Metacognição)
- Nível 5: Ação (Resolução, Criatividade, Decisão, Planejamento, Executivo)

**Estrutura**:
```
src/brain/
├── fundamental/      # Nível 1
│   ├── perception/
│   ├── attention/
│   └── memory/
├── cognitive/       # Nível 2
│   ├── thinking/
│   ├── language/
│   └── learning/
├── affective/        # Nível 3
│   ├── emotion/
│   └── motivation/
├── metacognitive/    # Nível 4
│   ├── consciousness/
│   └── metacognition/
└── action/           # Nível 5
    ├── problem_solving/
    ├── creativity/
    ├── decision_making/
    ├── planning/
    └── executive/
```

**Vantagens**:
- ✅ Organização lógica
- ✅ Dependências claras
- ✅ Implementação incremental (nível por nível)

**Desvantagens**:
- ⚠️ Pode ser rígido
- ⚠️ Alguns processos podem não se encaixar bem

---

### Opção C: Arquitetura Baseada em Fluxo (Inspirada em SOAR)

**Descrição**:
- Processos organizados por fluxo de informação
- Entrada → Percepção → Atenção → Memória → Pensamento → Decisão → Ação
- Processos paralelos (Emoção, Motivação, Metacognição)

**Estrutura**:
```
src/brain/
├── input/            # Entrada
│   └── perception/
├── processing/       # Processamento
│   ├── attention/
│   ├── memory/
│   └── thinking/
├── parallel/         # Processos paralelos
│   ├── emotion/
│   ├── motivation/
│   └── metacognition/
└── output/           # Saída
    ├── decision_making/
    ├── planning/
    └── executive/
```

**Vantagens**:
- ✅ Fluxo natural de informação
- ✅ Processos paralelos claros
- ✅ Alinhado com arquiteturas cognitivas

**Desvantagens**:
- ⚠️ Pode não capturar todas as interações
- ⚠️ Alguns processos não se encaixam no fluxo linear

---

### Opção D: Arquitetura Híbrida (Modular + Hierárquica)

**Descrição**:
- Combina modularidade com organização hierárquica
- Processos são módulos independentes
- Organizados em níveis hierárquicos
- Comunicação via bus de eventos

**Estrutura**:
```
src/brain/
├── core/             # Núcleo (fundamentais)
│   ├── perception/
│   ├── attention/
│   └── memory/
├── cognitive/       # Cognitivos
│   ├── thinking/
│   ├── language/
│   └── learning/
├── affective/        # Afetivos
│   ├── emotion/
│   └── motivation/
├── metacognitive/    # Metacognitivos
│   ├── consciousness/
│   └── metacognition/
├── action/           # Ação
│   ├── problem_solving/
│   ├── creativity/
│   ├── decision_making/
│   ├── planning/
│   └── executive/
└── bus/              # Bus de eventos
    └── event_bus.py
```

**Vantagens**:
- ✅ Melhor dos dois mundos
- ✅ Modular e organizado
- ✅ Comunicação flexível (bus de eventos)
- ✅ Extensível

**Desvantagens**:
- ⚠️ Mais complexo
- ⚠️ Precisa gerenciar bus de eventos

---

## Recomendações

### Recomendação Principal: **Opção D (Híbrida)**

**Justificativa**:

1. **Modularidade**: Fácil adicionar/remover processos
2. **Organização**: Hierarquia clara de dependências
3. **Flexibilidade**: Bus de eventos permite comunicação flexível
4. **Extensibilidade**: Fácil adicionar novos processos
5. **Testabilidade**: Módulos podem ser testados independentemente

**Implementação Gradual**:
1. **Fase 1**: Core (Percepção, Atenção, Memória)
2. **Fase 2**: Cognitivos (Pensamento, Linguagem, Aprendizado)
3. **Fase 3**: Afetivos (Emoção, Motivação)
4. **Fase 4**: Metacognitivos (Consciência, Metacognição)
5. **Fase 5**: Ação (Resolução, Criatividade, Decisão, Planejamento, Executivo)

---

## Decisão Final

**ESCOLHA PENDENTE - Aguardando confirmação do decisor**

### Proposta de Decisão:

**Opção D: Arquitetura Híbrida (Modular + Hierárquica + Bus de Eventos)**

**Justificativa da Escolha**:
- Combina modularidade, organização e flexibilidade
- Permite implementação gradual
- Alinhado com arquiteturas cognitivas modernas
- Extensível e testável

**Plano de Implementação**:
1. Criar estrutura de diretórios
2. Implementar bus de eventos
3. Implementar processos fundamentais (Fase 1)
4. Expandir gradualmente (Fases 2-5)

---

## Impacto na Arquitetura

### Componentes Necessários:

1. **Bus de Eventos**:
   - Comunicação assíncrona entre processos
   - Pub/Sub pattern
   - Eventos tipados

2. **Interfaces de Processos**:
   - Interface base para todos os processos
   - Métodos padrão (process, update, reset)
   - Integração com bus

3. **Gerenciador de Processos**:
   - Orquestração de processos
   - Gerenciamento de dependências
   - Ciclo de vida

### Integração com AIOS:

- **Agendamento**: AIOS gerencia recursos
- **Contexto**: AIOS gerencia contexto
- **Memória**: AIOS + PostgreSQL + pgvector
- **Processos**: npllm implementa processos psicológicos sobre AIOS

---

## Próximas Decisões Dependentes

Esta decisão afeta:

1. **Decisão 004**: Implementação de Percepção
2. **Decisão 005**: Implementação de Atenção
3. **Decisão 006**: Implementação de Memória (hierarquia)
4. **Decisão 007**: Integração Backpropamine + RAG
5. **Decisão 008**: Sistema Dopaminérgico (RL)

---

## Referências

### Papers Acadêmicos

1. **ACT-R**: Anderson, J. R., & Lebiere, C. (1998). The Atomic Components of Thought
2. **SOAR**: Laird, J. E. (2012). The SOAR Cognitive Architecture
3. **CLARION**: Sun, R. (2006). CLARION: A Cognitive Architecture. ArXiv: cs/0602002
4. **Attention**: Vaswani, A., et al. (2017). Attention Is All You Need. ArXiv: 1706.03762
5. **RAG**: Lewis, P., et al. (2020). Retrieval-Augmented Generation. ArXiv: 2005.11401
6. **Backpropamine**: Miconi, T., et al. (2020). Backpropamine. ArXiv: 2002.10585
7. **Transformer-XL**: Dai, Z., et al. (2019). Transformer-XL. ArXiv: 1901.02860
8. **Memformer**: Wu, Y., et al. (2022). Memformer. ArXiv: 2201.08309

### Documentação do Projeto

- `PROCESSOS_PSICOLOGICOS.md` - Mapeamento completo dos 15 processos
- `PLANO_PROCESSOS_PSICOLOGICOS.md` - Plano de implementação detalhado

---

## Notas Adicionais

- **Implementação Gradual**: Começar com processos fundamentais
- **Testes**: Cada processo deve ser testável independentemente
- **Documentação**: Cada processo deve ter documentação clara
- **Performance**: Monitorar impacto de cada processo

---

**Próximo Passo**: Aguardar confirmação da decisão para prosseguir com Decisão 004 (Implementação de Percepção).

