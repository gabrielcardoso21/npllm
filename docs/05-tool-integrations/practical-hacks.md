# "Gambiarras" Práticas que Funcionam

## Introdução

Este documento compila técnicas práticas, "hacks" e soluções criativas que pessoas usam para fazer LLMs funcionarem melhor na prática. Muitas dessas técnicas não são formalmente documentadas em papers, mas são amplamente usadas na indústria.

## Técnicas Práticas

### 1. Prompt Engineering Avançado

#### Chain-of-Thought (CoT)
- **Conceito**: Pedir ao modelo para "pensar passo a passo"
- **Exemplo**: "Vamos resolver isso passo a passo..."
- **Por que funciona**: Força modelo a raciocinar explicitamente
- **Paper**: "Chain-of-Thought Prompting" (Wei et al., 2022)

#### Few-Shot Examples
- **Conceito**: Dar exemplos no prompt
- **Técnica**: Mostrar formato desejado
- **Por que funciona**: Modelo aprende padrão dos exemplos

#### Role-Playing
- **Conceito**: Pedir modelo para assumir papel específico
- **Exemplo**: "Você é um especialista em..."
- **Por que funciona**: Ativa conhecimento especializado

#### Temperature Tuning
- **Conceito**: Ajustar temperatura (0.0-2.0)
- **Baixa (0.0-0.3)**: Mais determinístico, melhor para tarefas específicas
- **Alta (0.7-1.0)**: Mais criativo, melhor para geração
- **Por que funciona**: Controla aleatoriedade

### 2. RAG Hacks

#### Chunking Inteligente
- **Overlap**: Chunks sobrepostos (50-100 tokens)
- **Semantic Chunking**: Dividir por significado, não tamanho
- **Hierarchical**: Chunks grandes + pequenos
- **Por que funciona**: Preserva contexto

#### Query Expansion
- **Sinônimos**: Expandir query com sinônimos
- **Hybrid Search**: Combinar busca densa e esparsa (BM25)
- **Multi-Query**: Gerar múltiplas queries
- **Por que funciona**: Melhora recall

#### Re-ranking
- **Cross-Encoder**: Re-ranquear resultados com modelo mais forte
- **Multi-stage**: Busca ampla, depois re-rank
- **Por que funciona**: Melhora precisão

### 3. Memory Hacks

#### Conversation Memory
- **Buffer Memory**: Últimas N mensagens
- **Summary Memory**: Resumir conversas antigas
- **Entity Memory**: Lembrar entidades mencionadas
- **Por que funciona**: Mantém contexto sem explodir tokens

#### External State
- **Database**: Armazenar estado em DB
- **Vector Store**: Armazenar memórias como embeddings
- **Key-Value Store**: Armazenar informações estruturadas
- **Por que funciona**: Escala melhor que contexto

### 4. Cost Optimization

#### Caching
- **Response Caching**: Cachear respostas similares
- **Embedding Caching**: Cachear embeddings
- **Por que funciona**: Reduz chamadas de API

#### Model Selection
- **Smaller Models**: Usar modelos menores quando possível
- **Local Models**: Usar modelos locais (Llama, Mistral)
- **Por que funciona**: Reduz custo

#### Batch Processing
- **Batch Requests**: Processar múltiplas requests juntas
- **Streaming**: Usar streaming quando possível
- **Por que funciona**: Mais eficiente

### 5. Reliability Hacks

#### Retry Logic
- **Exponential Backoff**: Retry com delay crescente
- **Fallback Models**: Usar modelo alternativo se falhar
- **Por que funciona**: Lida com falhas temporárias

#### Validation
- **Output Parsing**: Validar formato de saída
- **Schema Validation**: Validar contra schema
- **Por que funciona**: Previne erros downstream

#### Error Handling
- **Try-Catch**: Capturar erros graciosamente
- **Fallback Responses**: Respostas padrão se falhar
- **Por que funciona**: Sistema mais robusto

### 6. Performance Hacks

#### Streaming
- **Token Streaming**: Stream tokens conforme gerados
- **Por que funciona**: Melhora UX, parece mais rápido

#### Parallel Processing
- **Async Calls**: Chamadas assíncronas
- **Parallel Retrieval**: Buscar múltiplos documentos em paralelo
- **Por que funciona**: Reduz latência total

#### Pre-computation
- **Pre-compute Embeddings**: Embeddings offline
- **Pre-warm Cache**: Aquecer cache
- **Por que funciona**: Reduz latência

### 7. Quality Hacks

#### Self-Consistency
- **Multiple Samples**: Gerar múltiplas respostas
- **Voting**: Votar na melhor resposta
- **Por que funciona**: Reduz erros aleatórios

#### Self-Reflection
- **Self-Critique**: Modelo critica própria resposta
- **Revision**: Revisar e melhorar resposta
- **Por que funciona**: Melhora qualidade

#### Human-in-the-Loop
- **Validation**: Humanos validam respostas críticas
- **Feedback Loop**: Aprender com feedback
- **Por que funciona**: Garante qualidade

## Frameworks que Facilitam

### 1. LangChain
- **Memory Management**: Fácil gerenciar memória
- **Chains**: Composição de operações
- **Agents**: Agents prontos
- **Tools**: Muitas tools disponíveis

### 2. LlamaIndex
- **RAG Otimizado**: RAG muito otimizado
- **Query Planning**: Planejamento automático
- **Data Connectors**: Muitos conectores

### 3. Semantic Kernel (Microsoft)
- **Planners**: Planejamento automático
- **Plugins**: Sistema de plugins
- **Memory**: Gerenciamento de memória

## Anti-Patterns (O que NÃO fazer)

### 1. Context Explosion
- **Problema**: Context muito grande
- **Solução**: Resumir, chunking inteligente

### 2. Over-Prompting
- **Problema**: Prompts muito longos
- **Solução**: Ser conciso, usar few-shot eficientemente

### 3. Ignoring Errors
- **Problema**: Não tratar erros
- **Solução**: Validação, retry, fallbacks

### 4. Cost Ignorance
- **Problema**: Não monitorar custo
- **Solução**: Caching, model selection, monitoring

## Referências

### Recursos Online
- LangChain Discord: Comunidade ativa
- Reddit r/LangChain: Discussões
- GitHub Issues: Problemas e soluções
- LangChain Blog: https://blog.langchain.dev
- LlamaIndex Blog: https://blog.llamaindex.ai
- Awesome LangChain: Lista de recursos
- LangChain Templates: Templates prontos
- Community Examples: Exemplos da comunidade

