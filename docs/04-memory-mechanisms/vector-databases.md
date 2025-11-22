# Vector Databases para LLMs

## Introdução

Vector databases são sistemas especializados em armazenar e buscar embeddings (vetores de alta dimensão) de forma eficiente. São fundamentais para RAG e outros sistemas de memória externa em LLMs.

## Fundamentos Teóricos

### Conceito

**Embeddings**: Representações vetoriais de texto (ou outros dados)

**Similarity Search**: Busca por similaridade (cosine similarity, dot product, etc.)

**Índices**: Estruturas de dados otimizadas para busca vetorial

### Aplicações

- **RAG**: Retrieval de documentos relevantes
- **Semantic Search**: Busca semântica
- **Recommendation**: Sistemas de recomendação
- **Clustering**: Agrupamento de documentos similares

## Técnicas e Métodos

### 1. FAISS (Facebook AI Similarity Search)

**Desenvolvido por**: Facebook AI Research
- **GitHub**: https://github.com/facebookresearch/faiss

**Características**:
- Muito eficiente
- Múltiplos índices
- GPU support
- Open-source

**Índices**:
- **Flat**: Busca exaustiva (precisa, lenta)
- **IVF**: Inverted File Index (rápida, aproximada)
- **HNSW**: Hierarchical Navigable Small World (muito rápida)
- **LSH**: Locality Sensitive Hashing

**Vantagens**:
- Muito rápido
- Escalável
- Bem documentado

**Limitações**:
- Requer conhecimento técnico
- Não é database completa (só vectors)

### 2. ChromaDB

**Desenvolvido por**: Chroma
- **Website**: https://www.trychroma.com

**Características**:
- Fácil de usar
- API simples
- Metadata support
- Embedding functions integradas

**Vantagens**:
- Muito fácil de usar
- Boa para começar
- Metadata filtering
- Open-source

**Limitações**:
- Menos otimizado que FAISS
- Menos escalável

### 3. Pinecone

**Desenvolvido por**: Pinecone
- **Website**: https://www.pinecone.io

**Características**:
- Managed service
- Cloud-based
- Escalável
- Fácil de usar

**Vantagens**:
- Muito fácil de usar
- Escalável automaticamente
- Sem infraestrutura
- Boa performance

**Limitações**:
- Custo (pago)
- Vendor lock-in
- Menos controle

### 4. Weaviate

**Desenvolvido por**: SeMI Technologies
- **Website**: https://weaviate.io

**Características**:
- GraphQL API
- Vector + Graph
- Open-source
- Self-hosted ou cloud

**Vantagens**:
- Graph capabilities
- Boa performance
- Open-source
- Flexível

**Limitações**:
- Mais complexo
- Curva de aprendizado

### 5. Qdrant

**Desenvolvido por**: Qdrant
- **Website**: https://qdrant.tech

**Características**:
- Open-source
- Rust-based (rápido)
- API REST
- Boa performance

**Vantagens**:
- Muito rápido
- Open-source
- Boa documentação
- Self-hosted

### 6. Milvus

**Desenvolvido por**: Zilliz
- **Website**: https://milvus.io

**Características**:
- Open-source
- Escalável
- Distribuído
- Boa performance

**Vantagens**:
- Muito escalável
- Distribuído
- Open-source
- Boa performance

**Limitações**:
- Mais complexo
- Requer mais recursos

## Comparação

| Database | Tipo | Facilidade | Performance | Escalabilidade | Custo |
|----------|------|------------|-------------|----------------|------|
| FAISS | Library | Média | Muito Alta | Alta | Grátis |
| ChromaDB | Database | Alta | Média | Média | Grátis |
| Pinecone | Managed | Muito Alta | Alta | Muito Alta | Pago |
| Weaviate | Database | Média | Alta | Alta | Grátis |
| Qdrant | Database | Média | Muito Alta | Alta | Grátis |
| Milvus | Database | Baixa | Muito Alta | Muito Alta | Grátis |

## Implementações Práticas

### Integração com LangChain

```python
from langchain.vectorstores import FAISS, Chroma, Pinecone
from langchain.embeddings import OpenAIEmbeddings

# FAISS
vectorstore = FAISS.from_documents(docs, embeddings)

# ChromaDB
vectorstore = Chroma.from_documents(docs, embeddings)

# Pinecone
vectorstore = Pinecone.from_documents(docs, embeddings)
```

### Integração com LlamaIndex

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader

# Cria índice automaticamente
index = VectorStoreIndex.from_documents(documents)
```

## Casos de Uso

### 1. RAG
- Armazenar embeddings de documentos
- Buscar documentos relevantes

### 2. Semantic Search
- Busca semântica em corpus
- Encontrar documentos similares

### 3. Recommendation
- Recomendar itens similares
- Sistemas de recomendação

### 4. Clustering
- Agrupar documentos similares
- Análise de corpus

## Limitações e Desafios

### Desafios Técnicos

1. **Dimensionality**: Alta dimensionalidade
2. **Scalability**: Escalabilidade para bilhões de vectors
3. **Accuracy vs Speed**: Trade-off precisão/velocidade
4. **Updates**: Atualização de índices

### Limitações Atuais

- Alta dimensionalidade é desafiadora
- Updates podem ser lentos
- Requer tuning de índices
- Custo de armazenamento

## Direções Futuras

1. **Better Indices**: Índices mais eficientes
2. **Hybrid Search**: Combinação de busca densa e esparsa
3. **Real-time Updates**: Atualizações em tempo real
4. **Multimodal**: Suporte a múltiplas modalidades

## Referências

### Recursos Online
- FAISS: https://github.com/facebookresearch/faiss
- ChromaDB: https://www.trychroma.com
- Pinecone: https://www.pinecone.io
- Weaviate: https://weaviate.io
- Qdrant: https://qdrant.tech
- Milvus: https://milvus.io
- Papers with Code: Vector Search
- GitHub: Implementações open-source

