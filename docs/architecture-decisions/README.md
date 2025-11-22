# Decisões Técnicas de Arquitetura

Este diretório contém todas as decisões técnicas de alto e baixo nível tomadas durante o desenvolvimento do sistema Linux integrado com IA.

## Documento Educativo

Antes de começar as decisões, leia o documento educativo:

- **[000-educational-ia-linux-integration.md](./000-educational-ia-linux-integration.md)**: Guia completo sobre diferentes abordagens de integração de IA com Linux, incluindo AIOS, SchedCP, Deepin 25, SUSE AI, Red Hat AI e comparações detalhadas.

## Processo de Decisão

Cada decisão técnica segue este processo interativo:

1. **Pesquisa**: Pesquisa profunda na internet e papers relevantes
2. **Opções**: Apresentação de alternativas viáveis com prós/contras
3. **Recomendações**: Recomendações baseadas nos objetivos do projeto
4. **Decisão**: Documentação da escolha final e justificativa
5. **Arquitetura Detalhada**: Base para fase de arquitetura de baixo nível

## Estrutura de Documentos

Cada documento de decisão segue este formato:

```markdown
# Decisão Técnica N: [Título]

## Contexto
[Por que esta decisão é necessária]

## Objetivos
[O que queremos alcançar com esta decisão]

## Pesquisa e Estado da Arte
[Pesquisa profunda com referências]

## Opções Consideradas
[Alternativas com análise detalhada]

## Recomendações
[Recomendações baseadas nos objetivos]

## Decisão Final
[Escolha documentada com justificativa]

## Impacto na Arquitetura
[Como isso afeta o sistema]

## Próximas Decisões Dependentes
[Decisões que dependem desta]
```

## Índice de Decisões

### Fase 1: Integração com Sistema Linux

- [Decisão 001: Integração com Kernel Linux](./001-kernel-integration.md) - **EM ANDAMENTO**
- [Decisão 002: Escolha de Distribuição Linux para Servidor](./002-server-distribution-choice.md) - ✅ **ESCOLHIDA** (Ubuntu Server + AIOS)
- [Decisão 003: Arquitetura de Processos Psicológicos](./003-psychological-processes-architecture.md) - **EM ANDAMENTO**
- [Decisão 004: Arquitetura de Comunicação Kernel ↔ User Space](./004-kernel-communication.md) - Pendente
- [Decisão 003: Integração com systemd](./003-systemd-integration.md) - Pendente
- [Decisão 004: Monitoramento e Observabilidade do Sistema](./004-system-monitoring.md) - Pendente

### Fase 2: Sistema Sensorial (SNP)

- [Decisão 005: Arquitetura do Sistema Sensorial](./005-sensory-architecture.md) - Pendente
- [Decisão 006: Implementação de Visão (Leitura de Arquivos)](./006-vision-implementation.md) - Pendente
- [Decisão 007: Implementação de Tato (Monitoramento)](./007-touch-implementation.md) - Pendente
- [Decisão 008: Implementação de Audição (Eventos)](./008-hearing-implementation.md) - Pendente
- [Decisão 009: Implementação de Olfato (Detecção de Padrões)](./009-smell-implementation.md) - Pendente

### Fase 3: Sistema Motor (SNP)

- [Decisão 010: Arquitetura do Sistema Motor](./010-motor-architecture.md) - Pendente
- [Decisão 011: Tool Calling e Execução de Programas](./011-tool-calling.md) - Pendente
- [Decisão 012: Operações de Arquivo e Filesystem](./012-file-operations.md) - Pendente
- [Decisão 013: Segurança e Sandboxing](./013-security-sandboxing.md) - Pendente

### Fase 4: Sistema Nervoso Central (SNC)

- [Decisão 014: Integração Backpropamine + RAG](./014-learning-integration.md) - Pendente
- [Decisão 015: Arquitetura de Memória (Hipocampo)](./015-memory-architecture.md) - Pendente
- [Decisão 016: Sistema Dopaminérgico (RL)](./016-dopamine-system.md) - Pendente
- [Decisão 017: Plasticidade Sináptica (Backpropamine)](./017-synaptic-plasticity.md) - Pendente

### Fase 5: Processos Psicológicos

- [Decisão 018: Ordem de Implementação dos Processos Psicológicos](./018-psychological-processes-order.md) - Pendente
- [Decisão 019: Arquitetura de Percepção](./019-perception-architecture.md) - Pendente
- [Decisão 020: Arquitetura de Atenção](./020-attention-architecture.md) - Pendente

### Fase 6: Interface e Comunicação

- [Decisão 021: Protocolo de Comunicação SNC ↔ SNP](./021-communication-protocol.md) - Pendente
- [Decisão 022: Interface de Usuário](./022-user-interface.md) - Pendente
- [Decisão 023: API e Integrações Externas](./023-api-integrations.md) - Pendente

## Status das Decisões

- 🟢 **Concluída**: Decisão finalizada e documentada
- 🟡 **Em Andamento**: Decisão sendo discutida
- ⚪ **Pendente**: Decisão ainda não iniciada

## Como Contribuir

1. Para cada nova decisão, crie um documento seguindo o template
2. Realize pesquisa profunda antes de apresentar opções
3. Apresente pelo menos 3 opções viáveis
4. Documente a decisão final com justificativa clara
5. Atualize este README com o status

## Referências Gerais

- [AIOS: LLM Agent Operating System](https://arxiv.org/abs/2403.16971)
- [SchedCP: LLM Agent Framework for Linux Schedulers](https://arxiv.org/abs/2509.01245)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [Backpropamine Paper](https://arxiv.org/abs/2002.10585)

