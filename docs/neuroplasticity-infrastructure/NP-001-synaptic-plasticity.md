# Decisão NP-001: Plasticidade Sináptica - Infraestrutura Base

**Status**: 🟡 Em Andamento  
**Data**: 2025-01-27  
**Decisor**: Gabriel Cardoso  
**Contexto**: Neuroplasticidade é a base do projeto - sem ela, não há processos psicológicos  
**Dependências**: Nenhuma (decisão fundamental)

---

## Contexto

A neuroplasticidade é o mecanismo fundamental que permite ao cérebro adaptar-se e aprender. No contexto do npllm, a plasticidade sináptica é a infraestrutura base que permite:

1. **Aprendizado Contínuo**: Adaptação sem esquecimento catastrófico
2. **Memória Persistente**: Consolidação de conhecimento
3. **Adaptação Contextual**: Ajuste baseado em experiência
4. **Evolução do Sistema**: Melhoria contínua ao longo do tempo

**Sem neuroplasticidade, o sistema não pode aprender verdadeiramente** - apenas usar conhecimento pré-treinado.

---

## Pesquisa Profunda: Estado da Arte em Plasticidade Sináptica para LLMs

### 1. Plasticidade Sináptica Biológica

#### Fundamentos Neurocientíficos

**LTP (Long-Term Potentiation)**:
- Fortalecimento de sinapses após estimulação repetida
- Base para aprendizado e memória
- Persiste por horas a anos
- **Paper Clássico**: Bliss & Lomo (1973) - "Long-lasting potentiation of synaptic transmission"

**LTD (Long-Term Depression)**:
- Enfraquecimento de sinapses não utilizadas
- Eliminação de conexões desnecessárias
- Balanceamento com LTP
- **Mecanismo**: Timing-dependent, atividade-dependente

**Regra de Hebb (1949)**:
- "Neurônios que disparam juntos, conectam-se juntos"
- Base para aprendizado associativo
- Fundamenta muitos algoritmos modernos

**STDP (Spike-Timing Dependent Plasticity)**:
- Plasticidade baseada em timing preciso
- Se pré-sináptico dispara antes do pós: LTP
- Se pós-sináptico dispara antes do pré: LTD
- **Relevância**: Processamento temporal

---

### 2. Plasticidade Diferenciável (Differentiable Plasticity)

#### Paper Fundamental

**"Differentiable plasticity: training plastic neural networks with backpropagation"**  
**Autores**: Miconi, T., Clune, J., & Stanley, K. O. (2018)  
**ArXiv**: [1804.02464](https://arxiv.org/abs/1804.02464)

**Conceito**:
- Permite que redes neurais aprendam a modificar suas próprias conexões
- Cada conexão tem: **peso base** + **peso plástico**
- Peso plástico adapta-se baseado em atividade
- Treinável via backpropagation

**Mecanismo**:
```
Peso Total = Peso Base + (Peso Plástico × Atividade)
```

**Características**:
- ✅ Treinável via backpropagation
- ✅ Permite aprendizado contínuo
- ✅ Redes adaptam-se após treinamento inicial
- ✅ Baseado em neurociência real

**Aplicações Demonstradas**:
- Aprendizado contínuo sem esquecimento catastrófico
- Adaptação rápida a novas tarefas
- Memória de trabalho em redes neurais
- Transfer learning adaptativo

**Limitações Identificadas**:
- ⚠️ Overhead computacional (parâmetros adicionais)
- ⚠️ Testado principalmente em redes pequenas
- ⚠️ Hiperparâmetros precisam ajuste fino
- ⚠️ Não aplicado extensivamente em LLMs grandes

**Status Atual**:
- ✅ Código disponível (PyTorch, TensorFlow)
- ✅ Implementações open-source
- ⚠️ Não amplamente usado em produção
- ⚠️ Ainda área de pesquisa ativa

---

### 3. Backpropamine (Plasticidade Neuromodulada Diferenciável)

#### Paper Fundamental

**"Backpropamine: training self-modifying neural networks with differentiable neuromodulated plasticity"**  
**Autores**: Miconi, T., Rawal, A., Clune, J., & Stanley, K. O. (2020)  
**ArXiv**: [2002.10585](https://arxiv.org/abs/2002.10585)

**Conceito**:
- Estende plasticidade diferenciável com **neuromodulação**
- Neurônios moduladores aprendem a controlar plasticidade de outros
- Similar a neurotransmissores (dopamina, serotonina) no cérebro
- Aprendizado endógeno de quando e onde modular

**Mecanismo**:
```
Sinal Modulador = f(Estado, Contexto)
Plasticidade = Plasticidade Base × Sinal Modulador
```

**Características**:
- ✅ Neuromodulação aprendida endogenamente
- ✅ Controle dinâmico da plasticidade
- ✅ Melhor performance em RL e aprendizado supervisionado
- ✅ Baseado em neurociência real (dopamina, acetilcolina)

**Resultados Demonstrados**:
- Melhor performance em RL (até 2x)
- Aprendizado mais rápido
- Adaptação contextual
- Seleção de onde aprender

**Limitações Identificadas**:
- ⚠️ Complexidade adicional
- ⚠️ Testado principalmente em modelos pequenos
- ⚠️ Não aplicado em LLMs de grande escala
- ⚠️ Requer mais pesquisa

**Status Atual**:
- ✅ Código disponível
- ✅ Implementações em PyTorch/JAX
- ⚠️ Ainda experimental
- ⚠️ Não usado em produção LLMs

**Relevância para npllm**:
- ⭐⭐⭐⭐⭐ **CRÍTICO** - É exatamente o que o projeto precisa
- Alinhado com arquitetura biológica planejada
- Permite aprendizado contínuo real

---

### 4. Memory Aware Synapses (MAS)

#### Paper

**"Memory Aware Synapses: Learning what (not) to forget"**  
**Autores**: Aljundi, R., Babiloni, F., Elhoseiny, M., Rohrbach, M., & Tuytelaars, T. (2017)  
**ArXiv**: [1711.09601](https://arxiv.org/abs/1711.09601)

**Conceito**:
- Identifica automaticamente parâmetros importantes
- Baseado em gradientes (não requer dados de validação)
- Aprendizado não-supervisionado de importância

**Mecanismo**:
- Calcula importância baseada em magnitude de gradientes
- Preserva parâmetros importantes durante novo aprendizado
- Adaptativo e eficiente

**Vantagens**:
- ✅ Não requer labels
- ✅ Computacionalmente eficiente
- ✅ Adaptativo
- ✅ Já implementado no projeto npllm

**Limitações**:
- ⚠️ Pode ser conservador
- ⚠️ Não escala bem para modelos muito grandes
- ⚠️ Não é plasticidade real (é preservação)

**Status no Projeto**:
- ✅ Já implementado em `src/learning/continual_learning.py`
- ✅ Funcional e testado
- ⚠️ MAS sozinho não é suficiente (precisa de Backpropamine)

---

### 5. Elastic Weight Consolidation (EWC)

#### Paper

**"Overcoming catastrophic forgetting in neural networks"**  
**Autores**: Kirkpatrick, J., et al. (2017)  
**PNAS**, 114(13), 3521-3526

**Conceito**:
- Calcula importância de parâmetros (Fisher Information Matrix)
- Adiciona penalidade para mudanças em parâmetros importantes
- Permite adaptação de parâmetros menos importantes

**Vantagens**:
- ✅ Preserva conhecimento importante
- ✅ Relativamente simples
- ✅ Bem estudado

**Limitações**:
- ⚠️ Cálculo de Fisher Information é caro
- ⚠️ Não escala bem para muitas tarefas
- ⚠️ Pode ser muito conservador
- ⚠️ Não é plasticidade real (é preservação)

**Status**:
- ✅ Implementações disponíveis
- ✅ Usado em alguns sistemas
- ⚠️ Não é solução completa

---

### 6. Aplicação em LLMs: Estado Atual

#### O Que Existe Hoje

**1. Fine-tuning Tradicional**:
- ✅ Amplamente usado
- ✅ Funciona bem para adaptação
- ❌ Causa esquecimento catastrófico
- ❌ Não é plasticidade real

**2. LoRA (Low-Rank Adaptation)**:
- ✅ Eficiente computacionalmente
- ✅ Preserva modelo base
- ❌ Não é plasticidade real (é adapter)
- ❌ Não existe no cérebro

**3. In-Context Learning**:
- ✅ Aprendizado temporário no contexto
- ✅ Não modifica pesos
- ❌ Não é persistente
- ❌ Não é plasticidade real

**4. RAG (Retrieval-Augmented Generation)**:
- ✅ Memória externa
- ✅ Não modifica modelo
- ❌ Não consolida em parâmetros
- ❌ Não é plasticidade real

**5. Continual Learning Técnicas**:
- ✅ EWC, MAS, Replay
- ✅ Preservam conhecimento
- ❌ Não são plasticidade real
- ❌ Focam em preservação, não adaptação

#### O Que NÃO Existe Hoje

**1. Plasticidade Real em LLMs Grandes**:
- ❌ Backpropamine não foi aplicado em LLMs de 7B+ parâmetros
- ❌ Differentiable Plasticity não foi testado extensivamente
- ❌ Ainda área de pesquisa

**2. Plasticidade Eficiente**:
- ❌ Overhead computacional é alto
- ❌ Não escalável para modelos muito grandes
- ❌ Precisa de otimizações

**3. Plasticidade Integrada**:
- ❌ Não há framework completo
- ❌ Integração com RAG é experimental
- ❌ Consolidação durante "sono" não implementada

**4. Plasticidade em Produção**:
- ❌ Nenhum sistema de produção usa plasticidade real
- ❌ Ainda experimental
- ❌ Precisa mais pesquisa

---

### 7. Implementações Disponíveis

#### Código Open Source

**1. Backpropamine**:
- ✅ Código oficial disponível
- ✅ Implementações em PyTorch/JAX
- ⚠️ Focado em redes pequenas
- ⚠️ Não adaptado para Transformers/LLMs

**2. Differentiable Plasticity**:
- ✅ Implementações em PyTorch
- ✅ Exemplos disponíveis
- ⚠️ Não para LLMs

**3. MAS/EWC**:
- ✅ Implementações amplamente disponíveis
- ✅ Já usado no projeto
- ⚠️ Não é plasticidade real

#### Frameworks

**1. PyTorch**:
- ✅ Suporte para gradientes customizados
- ✅ Permite implementação de plasticidade
- ✅ Flexível

**2. JAX**:
- ✅ Facilita implementação de plasticidade
- ✅ Performance boa
- ✅ Gradientes automáticos

**3. TensorFlow**:
- ✅ Suporte para operações customizadas
- ✅ Permite implementação
- ⚠️ Menos flexível que PyTorch

---

### 8. Desafios e Limitações Atuais

#### Desafios Técnicos

1. **Escalabilidade**:
   - Plasticidade adiciona parâmetros (pesos plásticos)
   - Para LLM de 7B, adiciona ~7B parâmetros plásticos
   - Overhead de memória e computação

2. **Estabilidade**:
   - Balancear adaptação vs. estabilidade
   - Evitar instabilidade durante aprendizado
   - Hiperparâmetros críticos

3. **Eficiência Computacional**:
   - Cálculo de plasticidade adiciona overhead
   - Precisa otimizações específicas
   - Pode ser lento em modelos grandes

4. **Integração**:
   - Integrar com RAG
   - Integrar com consolidação
   - Integrar com sistema dopaminérgico

#### Limitações de Pesquisa

1. **Poucos Testes em LLMs Grandes**:
   - Maioria dos testes em redes pequenas
   - Não sabemos se escala para 7B+
   - Precisa validação

2. **Falta de Benchmarks**:
   - Não há benchmarks padronizados
   - Difícil comparar abordagens
   - Métricas não padronizadas

3. **Falta de Frameworks**:
   - Não há framework completo
   - Cada implementação é custom
   - Falta abstrações

---

## Estado Atual: O Que Temos

### ✅ Disponível e Funcional

1. **Backpropamine**:
   - ✅ Código disponível
   - ✅ Paper completo
   - ✅ Implementações funcionais
   - ⚠️ Não testado em LLMs grandes

2. **Differentiable Plasticity**:
   - ✅ Código disponível
   - ✅ Paper completo
   - ✅ Implementações funcionais
   - ⚠️ Não testado em LLMs grandes

3. **MAS (Memory Aware Synapses)**:
   - ✅ Já implementado no projeto
   - ✅ Funcional e testado
   - ✅ Eficiente
   - ⚠️ Não é plasticidade real (é preservação)

4. **Frameworks de Suporte**:
   - ✅ PyTorch (gradientes customizados)
   - ✅ JAX (facilita implementação)
   - ✅ TensorFlow (suporte básico)

### ⚠️ Parcialmente Disponível

1. **Continual Learning**:
   - ✅ Técnicas disponíveis (EWC, MAS, Replay)
   - ⚠️ Não são plasticidade real
   - ⚠️ Focam em preservação

2. **Fine-tuning**:
   - ✅ Amplamente usado
   - ⚠️ Causa esquecimento
   - ⚠️ Não é aprendizado contínuo

---

## Estado Atual: O Que NÃO Temos

### ❌ Não Disponível

1. **Plasticidade Real em LLMs Grandes**:
   - ❌ Backpropamine não aplicado em 7B+
   - ❌ Differentiable Plasticity não testado extensivamente
   - ❌ Ainda área de pesquisa

2. **Plasticidade Eficiente**:
   - ❌ Overhead computacional alto
   - ❌ Não otimizado para Transformers
   - ❌ Precisa otimizações específicas

3. **Framework Completo**:
   - ❌ Não há framework integrado
   - ❌ Cada implementação é custom
   - ❌ Falta abstrações

4. **Plasticidade em Produção**:
   - ❌ Nenhum sistema usa em produção
   - ❌ Ainda experimental
   - ❌ Precisa validação

5. **Integração Completa**:
   - ❌ Backpropamine + RAG não integrado
   - ❌ Consolidação durante "sono" não implementada
   - ❌ Sistema dopaminérgico não integrado

---

## Opções Consideradas

### Opção A: Backpropamine Puro

**Descrição**:
- Implementar Backpropamine conforme paper original
- Aplicar diretamente no LLM base
- Plasticidade real em todas as camadas

**Vantagens**:
- ✅ Plasticidade real (baseada em neurociência)
- ✅ Aprendizado contínuo verdadeiro
- ✅ Alinhado com objetivos do projeto
- ✅ Código disponível

**Desvantagens**:
- ⚠️ Overhead alto (dobra parâmetros)
- ⚠️ Não testado em LLMs grandes
- ⚠️ Pode ser instável
- ⚠️ Requer otimizações

**Implementação**:
- Usar código oficial Backpropamine
- Adaptar para Transformers
- Integrar com LLM base

**Custo Computacional**:
- Memória: ~2x (pesos base + plásticos)
- Computação: ~1.5x (cálculo de plasticidade)

---

### Opção B: Backpropamine Seletivo

**Descrição**:
- Backpropamine apenas em camadas específicas
- Exemplo: apenas em camadas de atenção ou feed-forward
- Reduz overhead mantendo plasticidade

**Vantagens**:
- ✅ Plasticidade real
- ✅ Overhead reduzido
- ✅ Mais eficiente
- ✅ Pode ser mais estável

**Desvantagens**:
- ⚠️ Plasticidade limitada
- ⚠️ Precisa decidir quais camadas
- ⚠️ Pode não ser suficiente

**Implementação**:
- Identificar camadas críticas
- Aplicar Backpropamine seletivamente
- Monitorar performance

**Custo Computacional**:
- Memória: ~1.2-1.5x (depende de camadas)
- Computação: ~1.2x

---

### Opção C: Backpropamine + MAS Híbrido

**Descrição**:
- Backpropamine para adaptação rápida
- MAS para preservação de conhecimento importante
- Combina adaptação e preservação

**Vantagens**:
- ✅ Plasticidade real (Backpropamine)
- ✅ Preservação (MAS)
- ✅ Balanceamento adaptação/preservação
- ✅ MAS já implementado

**Desvantagens**:
- ⚠️ Complexidade adicional
- ⚠️ Dois mecanismos para gerenciar
- ⚠️ Pode ser redundante

**Implementação**:
- Backpropamine para mudanças
- MAS para identificar importância
- Integração cuidadosa

**Custo Computacional**:
- Memória: ~2x (Backpropamine) + overhead MAS
- Computação: ~1.5x

---

### Opção D: Differentiable Plasticity (Sem Neuromodulação)

**Descrição**:
- Usar Differentiable Plasticity básico (sem neuromodulação)
- Mais simples que Backpropamine
- Plasticidade real mas sem controle contextual

**Vantagens**:
- ✅ Plasticidade real
- ✅ Mais simples que Backpropamine
- ✅ Menos parâmetros
- ✅ Código disponível

**Desvantagens**:
- ⚠️ Sem neuromodulação (menos controle)
- ⚠️ Não tão biológico quanto Backpropamine
- ⚠️ Pode ser menos eficiente

**Implementação**:
- Usar código Differentiable Plasticity
- Adaptar para Transformers
- Integrar com sistema

**Custo Computacional**:
- Memória: ~2x
- Computação: ~1.3x

---

### Opção E: MAS + Fine-tuning Incremental

**Descrição**:
- Manter MAS (já implementado)
- Fine-tuning incremental com preservação MAS
- Não é plasticidade real, mas funcional

**Vantagens**:
- ✅ MAS já implementado
- ✅ Funcional e testado
- ✅ Baixo overhead
- ✅ Prático

**Desvantagens**:
- ❌ Não é plasticidade real
- ❌ Não alinhado com objetivos (neuroplasticidade)
- ❌ Fine-tuning ainda causa algum esquecimento
- ❌ Não é revolucionário

**Implementação**:
- Usar MAS existente
- Fine-tuning com preservação
- Consolidação periódica

**Custo Computacional**:
- Memória: ~1.1x (overhead MAS)
- Computação: ~1.1x

---

## Recomendações

### Recomendação Principal: **Opção C (Backpropamine + MAS Híbrido)**

**Justificativa**:

1. **Alinhamento com Objetivos**:
   - ✅ Plasticidade real (Backpropamine) - nome do projeto
   - ✅ Preservação (MAS) - já implementado
   - ✅ Aprendizado contínuo verdadeiro

2. **Balanceamento**:
   - Backpropamine: Adaptação rápida e contextual
   - MAS: Preservação de conhecimento importante
   - Juntos: Melhor dos dois mundos

3. **Viabilidade**:
   - MAS já funciona no projeto
   - Backpropamine tem código disponível
   - Implementação incremental possível

4. **Biológico**:
   - Backpropamine baseado em neurociência real
   - MAS identifica importância (como cérebro)
   - Alinhado com arquitetura biológica

5. **Extensibilidade**:
   - Base sólida para adicionar outros mecanismos
   - Integração com RAG possível
   - Integração com sistema dopaminérgico possível

**Plano de Implementação**:
1. **Fase 1**: Implementar Backpropamine básico
2. **Fase 2**: Integrar com MAS existente
3. **Fase 3**: Otimizar para LLMs grandes
4. **Fase 4**: Integrar com RAG e consolidação

### Recomendação Secundária: **Opção B (Backpropamine Seletivo)** se overhead for muito alto

Se o overhead completo for proibitivo, começar com Backpropamine seletivo e expandir depois.

---

## Decisão Final

**ESCOLHA PENDENTE - Aguardando confirmação do decisor**

### Proposta de Decisão:

**Opção C: Backpropamine + MAS Híbrido**

**Justificativa da Escolha**:
- Combina plasticidade real (Backpropamine) com preservação (MAS)
- Alinhado com objetivos do projeto (neuroplasticidade)
- Implementação incremental possível
- Base sólida para expansão

**Plano de Implementação**:
1. Implementar Backpropamine básico
2. Integrar com MAS existente
3. Testar em modelo pequeno primeiro
4. Escalar para LLM completo
5. Otimizar performance

---

## Implicações para o Projeto

### Arquitetura

**Componentes Necessários**:
1. **Backpropamine Layer**:
   - Camada que adiciona pesos plásticos
   - Cálculo de plasticidade
   - Integração com neuromodulação

2. **MAS Integration**:
   - Identificação de importância
   - Preservação durante Backpropamine
   - Balanceamento adaptação/preservação

3. **Plasticity Manager**:
   - Orquestração de plasticidade
   - Controle de quando/onde aplicar
   - Integração com sistema dopaminérgico

### Estrutura de Código

```
src/brain/plasticity/
├── __init__.py
├── backpropamine.py      # Implementação Backpropamine
├── mas_integration.py    # Integração com MAS
├── plasticity_manager.py # Gerenciador de plasticidade
└── neuromodulation.py    # Neuromodulação (futuro)
```

### Recursos Necessários

**Memória**:
- Base: ~7GB (LLM 7B quantizado)
- Backpropamine: +7GB (pesos plásticos)
- Total: ~14GB (pode ser otimizado)

**Computação**:
- Overhead: ~50% adicional
- Pode ser otimizado com implementação eficiente

### Integração com Outros Componentes

1. **RAG (Hipocampo)**:
   - Backpropamine consolida memórias importantes
   - MAS identifica o que consolidar

2. **Sistema Dopaminérgico**:
   - Neuromodulação controla plasticidade
   - Recompensa guia aprendizado

3. **Consolidação Durante "Sono"**:
   - Backpropamine consolida em modelo base
   - MAS preserva conhecimento importante

---

## Próximas Decisões Dependentes

Esta decisão afeta:

1. **NP-002**: Consolidação de Memória
   - Depende de como Backpropamine funciona

2. **NP-003**: Neuromodulação
   - Integração com Backpropamine

3. **NP-006**: Integração Backpropamine + RAG
   - Como integrar plasticidade com memória externa

4. **NP-007**: Sistema Dopaminérgico
   - Como neuromodulação controla plasticidade

---

## Referências

### Papers Acadêmicos

1. **Differentiable plasticity: training plastic neural networks with backpropagation**
   - Miconi, T., Clune, J., & Stanley, K. O. (2018)
   - ArXiv: [1804.02464](https://arxiv.org/abs/1804.02464)

2. **Backpropamine: training self-modifying neural networks with differentiable neuromodulated plasticity**
   - Miconi, T., Rawal, A., Clune, J., & Stanley, K. O. (2020)
   - ArXiv: [2002.10585](https://arxiv.org/abs/2002.10585)

3. **Memory Aware Synapses: Learning what (not) to forget**
   - Aljundi, R., et al. (2017)
   - ArXiv: [1711.09601](https://arxiv.org/abs/1711.09601)

4. **Overcoming catastrophic forgetting in neural networks**
   - Kirkpatrick, J., et al. (2017)
   - PNAS, 114(13), 3521-3526

### Documentação do Projeto

- `docs/01-neuroplasticity-processes/synaptic-plasticity.md` - Documentação completa
- `ARQUITETURA_BIOLOGICA.md` - Arquitetura baseada em neurociência
- `src/learning/continual_learning.py` - Implementação MAS atual

### Recursos Online

- Backpropamine GitHub: Código oficial
- Papers with Code: Differentiable Plasticity
- ArXiv: cs.NE (Neural and Evolutionary Computing)

---

## Notas Adicionais

- **Validação Necessária**: Testar Backpropamine em modelo pequeno primeiro
- **Otimizações**: Pesquisar otimizações específicas para Transformers
- **Benchmarks**: Criar benchmarks para medir plasticidade
- **Documentação**: Documentar cada etapa da implementação

---

**Próximo Passo**: Aguardar confirmação da decisão para prosseguir com NP-002 (Consolidação de Memória).

