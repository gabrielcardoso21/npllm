# Guia Prático de Implementação

## Introdução

Este guia fornece passos práticos para implementar técnicas de neuroplasticidade em LLMs, com exemplos de código e frameworks recomendados.

## Quick Start: RAG (Mais Prático)

### Passo 1: Instalar Dependências

```bash
pip install langchain openai chromadb
```

### Passo 2: Código Básico

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# 1. Carregar documentos
documents = load_documents("docs/")

# 2. Dividir em chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
texts = text_splitter.split_documents(documents)

# 3. Criar embeddings e vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# 4. Criar chain
llm = OpenAI()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 5. Usar
response = qa_chain.run("What is neuroplasticity?")
```

## Implementação: EWC para Continual Learning

### Framework: Avalanche

```python
from avalanche.training import EWC
from avalanche.models import SimpleMLP
import torch

# 1. Criar modelo
model = SimpleMLP(num_classes=10)

# 2. Configurar EWC
strategy = EWC(
    model,
    torch.optim.SGD(model.parameters(), lr=0.001),
    EWC.ewc_loss,
    ewc_lambda=0.4,
    train_mb_size=32,
    train_epochs=1
)

# 3. Treinar em tarefas sequenciais
for experience in benchmark.train_stream:
    strategy.train(experience)
    strategy.eval(benchmark.test_stream)
```

## Implementação: Tool Calling

### OpenAI Function Calling

```python
import openai

functions = [
    {
        "name": "get_weather",
        "description": "Get weather for location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in São Paulo?"}],
    functions=functions,
    function_call="auto"
)
```

## Frameworks Recomendados

### Para RAG
- **LangChain**: Mais completo, fácil de usar
- **LlamaIndex**: Otimizado para RAG
- **Haystack**: Boa para produção

### Para Continual Learning
- **Avalanche**: Framework completo
- **Continuum**: Alternativa leve

### Para Vector Databases
- **FAISS**: Muito eficiente
- **ChromaDB**: Fácil de usar
- **Pinecone**: Managed service

## Troubleshooting

### Problema: RAG retorna resultados irrelevantes

**Soluções**:
1. Ajustar chunk size (tente 500-2000)
2. Melhorar embeddings (use modelos melhores)
3. Adicionar re-ranking
4. Ajustar número de documentos retornados

### Problema: EWC não preserva conhecimento

**Soluções**:
1. Aumentar `ewc_lambda` (tente 0.5-1.0)
2. Verificar cálculo de Fisher Information
3. Considerar usar Replay também

### Problema: Tool Calling não funciona

**Soluções**:
1. Verificar formato do schema
2. Usar modelo que suporta (GPT-3.5+, Claude)
3. Validar parâmetros

## Referências

- LangChain Docs: https://python.langchain.com
- Avalanche Docs: https://avalanche.continualai.org
- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling

