# 🌊 Status/Progress API (Fake Streaming)

A API npllm suporta "fake streaming" - envia status de progresso usando Server-Sent Events (SSE) ao invés de tokens reais.

## 📡 Endpoint com Streaming

### `/query` com `stream=true`

```bash
curl -N -X POST "http://161.97.123.192:8000/query?stream=true" \
  -H "Content-Type: application/json" \
  -d '{"query": "Crie uma função Python para calcular fibonacci"}'
```

### Formato SSE (Status/Progress)

A resposta vem em formato Server-Sent Events com status de progresso:

```
data: {"type": "status", "stage": "starting", "message": "Iniciando processamento..."}

data: {"type": "status", "stage": "context", "message": "Buscando contexto do curso..."}

data: {"type": "status", "stage": "adapter_selection", "message": "Selecionando adapter apropriado..."}

data: {"type": "status", "stage": "adapter_selected", "message": "Adapter selecionado: python_adapter"}

data: {"type": "status", "stage": "adapter_loading", "message": "Carregando adapter python_adapter..."}

data: {"type": "status", "stage": "adapter_loaded", "message": "Adapter python_adapter carregado com sucesso"}

data: {"type": "status", "stage": "generating", "message": "Gerando resposta..."}

data: {"type": "status", "stage": "processing", "message": "Processando resposta..."}

data: {"type": "status", "stage": "finalizing", "message": "Finalizando..."}

data: {"type": "done", "response": "def fibonacci(n): ...", "adapter_used": "python_adapter", "adapter_applied": true, "message": "Resposta gerada com sucesso"}
```

## 📝 Exemplo Python

```python
import requests
import json

url = "http://161.97.123.192:8000/query"
params = {"stream": True}
data = {"query": "Crie uma função Python para calcular fibonacci"}

response = requests.post(url, params=params, json=data, stream=True)

for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data: '):
            event_data = json.loads(line_str[6:])  # Remove "data: "
            
            if event_data['type'] == 'status':
                stage = event_data['stage']
                message = event_data['message']
                print(f"📊 [{stage}] {message}")
            elif event_data['type'] == 'done':
                print(f"\n✅ {event_data['message']}")
                print(f"📝 Resposta: {event_data['response']}")
                print(f"🔧 Adapter: {event_data['adapter_used']} (aplicado: {event_data['adapter_applied']})")
```

## 📝 Exemplo JavaScript

```javascript
const eventSource = new EventSource(
  'http://161.97.123.192:8000/query?stream=true',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: 'Crie uma função Python' })
  }
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'status') {
    // Atualiza UI com status
    document.getElementById('status').innerText = data.message;
    document.getElementById('progress').setAttribute('data-stage', data.stage);
  } else if (data.type === 'done') {
    eventSource.close();
    document.getElementById('output').innerText = data.response;
    console.log('Completo!', data);
  }
};
```

## 🔄 Modo Normal (sem streaming)

Para respostas completas de uma vez:

```bash
curl -X POST "http://161.97.123.192:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Crie uma função Python"}'
```

## ⚡ Vantagens do Status/Progress

1. **Feedback claro**: Usuário sabe exatamente o que está acontecendo
2. **Melhor UX**: Não fica esperando sem saber o status
3. **Debugging**: Identifica em qual etapa está o problema
4. **Progresso visível**: Sabe que o sistema está funcionando
5. **Mais simples**: Não precisa lidar com tokens individuais
6. **Adapter funciona**: Adapter é aplicado antes da geração completa

## 🎯 Tipos de Eventos

- `status`: Status de progresso (vários eventos)
  - `stage`: Etapa atual (`starting`, `context`, `adapter_selection`, `adapter_selected`, `adapter_loading`, `adapter_loaded`, `model_loading`, `generating`, `processing`, `finalizing`)
  - `message`: Mensagem descritiva
- `done`: Geração completa
  - `response`: Resposta completa gerada
  - `adapter_used`: Adapter usado
  - `adapter_applied`: Se adapter foi aplicado
  - `message`: Mensagem final

