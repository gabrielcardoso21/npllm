# 🌐 API npllm

API REST para comunicação com o sistema npllm.

## 🚀 Iniciar API

### Local

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Iniciar API
python -m src.api.server

# Ou usar script
./INICIAR_API.sh
```

### Servidor (Contabo)

```bash
ssh root@161.97.123.192
cd /opt/npllm
source .venv/bin/activate
python -m src.api.server --host 0.0.0.0 --port 8000
```

## 📚 Documentação Interativa

Após iniciar a API, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Principais

### 1. Health Check

```bash
GET /health
```

Retorna status do sistema.

### 2. Processar Query

```bash
POST /query
Content-Type: application/json

{
  "query": "Crie uma função Python para calcular fibonacci",
  "project_path": "/path/to/project",
  "file_path": "src/utils.py",
  "course_context": 1
}
```

**Resposta:**
```json
{
  "response": "def fibonacci(n): ...",
  "adapter_used": "python_adapter",
  "course_context_used": true
}
```

### 3. Capturar Feedback

```bash
POST /feedback
Content-Type: application/json

{
  "query": "Crie uma função Python...",
  "response": "def fibonacci(n): ...",
  "user_reaction": "Perfeito! Exatamente o que eu precisava!",
  "user_action": "accept",
  "explicit_feedback": 1.0
}
```

### 4. Criar Curso

```bash
POST /courses
Content-Type: application/json

{
  "name": "Odoo 18 Development",
  "description": "Aprender desenvolvimento de módulos Odoo 18",
  "source_type": "url",
  "source_path": "https://www.odoo.com/documentation/18.0/developer/"
}
```

### 5. Listar Cursos

```bash
GET /courses
```

### 6. Iniciar Aprendizado

```bash
POST /courses/{course_id}/start
```

### 7. Validar Curso

```bash
POST /courses/{course_id}/validate
Content-Type: application/json

{
  "automatic": true,
  "num_questions": 10,
  "validation_threshold": 0.75
}
```

### 8. Obter Conceitos Aprendidos

```bash
GET /courses/{course_id}/concepts
```

### 9. Acionar Sono (Consolidação)

```bash
POST /sleep?force=true
```

## 📝 Exemplos de Uso

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Criar curso
response = requests.post(f"{BASE_URL}/courses", json={
    "name": "FastAPI",
    "description": "Aprender FastAPI",
    "source_type": "url",
    "source_path": "https://fastapi.tiangolo.com/"
})
course = response.json()
course_id = course["id"]

# Iniciar aprendizado
requests.post(f"{BASE_URL}/courses/{course_id}/start")

# Processar query
response = requests.post(f"{BASE_URL}/query", json={
    "query": "Crie uma API FastAPI com autenticação JWT",
    "course_context": course_id
})
result = response.json()
print(result["response"])

# Capturar feedback
requests.post(f"{BASE_URL}/feedback", json={
    "query": "Crie uma API FastAPI...",
    "response": result["response"],
    "user_reaction": "Excelente!",
    "user_action": "accept"
})
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Criar curso
curl -X POST http://localhost:8000/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Odoo 18",
    "source_type": "url",
    "source_path": "https://www.odoo.com/documentation/18.0/"
  }'

# Processar query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Crie um módulo Odoo básico"
  }'
```

## 🔒 Segurança

Para produção, considere:

- Autenticação (JWT, API keys)
- HTTPS/TLS
- Rate limiting
- Validação de inputs
- Logs de auditoria

## 📊 Monitoramento

- Health check: `GET /health`
- Status: `GET /status`
- Logs: Verificar logs do sistema

