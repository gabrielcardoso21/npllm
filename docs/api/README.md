# API Documentation

## Endpoints

### POST /query
Processa query do usuário

**Request:**
```json
{
  "query": "Como criar um modelo Odoo?",
  "project_path": "/path/to/project",
  "project_id": "project_123"
}
```

**Response:**
```json
{
  "response": "Para criar um modelo Odoo...",
  "selected_adapters": ["odoo"],
  "adapter_probs": [0.8, 0.2],
  "modulation_intensities": [0.9, 0.1],
  "rag_used": true,
  "context_detected": "odoo",
  "latency": 1.23
}
```

### GET /health
Health check do sistema

**Response:**
```json
{
  "healthy": true,
  "memory": {
    "process_memory_mb": 2500,
    "system_memory_percent": 65.0
  },
  "cpu": {
    "process_cpu_percent": 45.0,
    "system_cpu_percent": 60.0
  }
}
```

### GET /metrics
Retorna métricas do sistema

**Response:**
```json
{
  "behavior": {
    "acceptance_rate": 0.75,
    "edit_rate": 0.20,
    "average_time_to_accept": 2.5
  },
  "learning": {
    "retention_tests": 10,
    "adaptation_tests": 5,
    "average_retention": 0.85,
    "average_adaptation": 0.15
  }
}
```

