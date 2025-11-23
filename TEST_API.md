# 🧪 Script de Teste da API

Script completo para testar todos os endpoints da API npllm, incluindo o **fake streaming** com status de progresso.

## 📋 Uso

### Teste completo (todos os endpoints)
```bash
python3 test_api.py
```

### Teste apenas streaming com query customizada
```bash
python3 test_api.py "Sua query aqui"
```

## 🎯 O que o script testa

1. **Health Check** (`/health`)
   - Verifica se API está online
   - Status do storage
   - Número de cursos

2. **Query Normal** (`/query` sem streaming)
   - Testa resposta completa de uma vez

3. **Query com Fake Streaming** (`/query?stream=true`)
   - **Testa status de progresso em tempo real**
   - Mostra todos os estágios:
     - 🚀 starting
     - 📚 context
     - 🔍 adapter_selection
     - ✅ adapter_selected
     - ⏳ adapter_loading
     - ✅ adapter_loaded / ⚠️ adapter_fallback
     - 🤖 model_loading
     - ⚙️ generating
     - 🔄 processing
     - ✨ finalizing
   - Exibe resposta completa no final

4. **Query com file_path** (`/query` com file_path)
   - Testa seleção automática de adapter baseado no arquivo

5. **Feedback** (`/feedback`)
   - Testa envio de feedback do usuário

6. **Cursos** (`/courses`)
   - Lista cursos disponíveis

## 📊 Exemplo de Saída

```
============================================================
  TESTE: Query com Fake Streaming (Status de Progresso)
============================================================
📝 Query: Crie uma função Python para calcular fibonacci

📡 Recebendo eventos SSE...

🚀 [starting            ] Iniciando processamento...
🔍 [adapter_selection   ] Selecionando adapter apropriado...
✅ [adapter_selected    ] Adapter selecionado: generic_adapter
⏳ [adapter_loading     ] Carregando adapter generic_adapter...
⚠️ [adapter_fallback    ] Adapter não encontrado, usando modelo base
🤖 [model_loading       ] Carregando modelo base...
⚙️ [generating          ] Gerando resposta...
🔄 [processing          ] Processando resposta...
✨ [finalizing          ] Finalizando...

============================================================
✅ Geração completa!
============================================================
🔧 Adapter usado: generic_adapter
🔧 Adapter aplicado: false

📝 Resposta completa (123 chars):
------------------------------------------------------------
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
------------------------------------------------------------
```

## ⚙️ Configuração

Edite as variáveis no início do script:

```python
API_BASE_URL = "http://161.97.123.192:8000"
TIMEOUT = 120  # 2 minutos para geração
```

## 🔧 Requisitos

```bash
pip install requests
```

## 📝 Notas

- O script trata erros de conexão gracefully
- Se a conexão for fechada antes do final, mas status foram recebidos, considera sucesso
- Timeout configurável para gerações longas
- Mostra resumo final com todos os testes

