# 🌊 Streaming API

A API npllm suporta streaming de respostas usando Server-Sent Events (SSE).

## 📡 Endpoint com Streaming

### `/query` com `stream=true`

```bash
curl -N -X POST "http://161.97.123.192:8000/query?stream=true" \
  -H "Content-Type: application/json" \
  -d '{"query": "Crie uma função Python para calcular fibonacci"}'
```

### Formato SSE

A resposta vem em formato Server-Sent Events:

```
data: {"type": "start", "adapter": "loading"}

data: {"type": "adapter", "adapter": "python_adapter"}

data: {"type": "token", "token": "def"}

data: {"type": "token", "token": " fibonacci"}

data: {"type": "token", "token": "(n):"}

...

data: {"type": "done", "response": "def fibonacci(n): ...", "adapter_used": "python_adapter"}
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
            
            if event_data['type'] == 'start':
                print("🚀 Iniciando geração...")
            elif event_data['type'] == 'adapter':
                print(f"🔧 Adapter: {event_data['adapter']}")
            elif event_data['type'] == 'token':
                print(event_data['token'], end='', flush=True)
            elif event_data['type'] == 'done':
                print(f"\n✅ Completo! Adapter: {event_data['adapter_used']}")
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
  
  if (data.type === 'token') {
    document.getElementById('output').innerText += data.token;
  } else if (data.type === 'done') {
    eventSource.close();
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

## ⚡ Vantagens do Streaming

1. **Feedback imediato**: Vê tokens sendo gerados em tempo real
2. **Melhor UX**: Usuário não fica esperando sem feedback
3. **Debugging**: Identifica problemas mais rápido
4. **Progresso visível**: Sabe que o sistema está funcionando

## 🎯 Tipos de Eventos

- `start`: Geração iniciada
- `adapter`: Adapter selecionado
- `token`: Token gerado (vários eventos)
- `done`: Geração completa

