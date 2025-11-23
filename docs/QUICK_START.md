# Quick Start Guide

Get npllm up and running in minutes.

## Prerequisites

- Python 3.11+
- PostgreSQL 14+ (or Docker)
- 8GB+ RAM recommended
- Internet connection (for API models)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/gabrielkmee/npllm.git
cd npllm
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL

**Option A: Using Docker (Recommended)**

```bash
docker compose up -d postgres
```

**Option B: Manual Installation**

Install PostgreSQL with pgvector extension, then create database:

```sql
CREATE DATABASE npllm;
CREATE EXTENSION vector;
```

### 5. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 6. Initialize System

```bash
python3 -m src.main --help
```

## Basic Usage

### Start API Server

```bash
./INICIAR_API.sh
# Or: python3 -m src.api
```

API will be available at `http://localhost:8000`

### Start Web Interface

```bash
./INICIAR_WEB.sh
# Or: python3 -m src.web
```

Web interface will be available at `http://localhost:7860`

### Test Direct Model

```bash
python3 testar_modelo_direto.py "Your question here"
```

## Example: Train a Course

```python
from src.main import initialize_system

# Initialize system
system = initialize_system()

# Create course
course = system.create_course(
    name="Python Best Practices",
    description="Learn Python best practices",
    source_type="url",
    source_path="https://docs.python.org/3/tutorial/"
)

# Train course
result = system.start_course_learning(course['id'])
print(f"Learned {result['learning']['concepts_learned']} concepts")

# Query with course context
response = system.process_query(
    "What are Python best practices?",
    course_context=course['id']
)
print(response['response'])
```

## Example: Test Learning

```bash
# Test learning with Odoo 18 course
python3 validar_aprendizado_odoo.py

# Test RAG functionality
python3 testar_rag_odoo.py

# Test conversation history and sleep
python3 validar_historico_sono.py
```

## Integration with Cursor IDE

1. **Start Cursor adapter**:
```bash
./INICIAR_CURSOR_ADAPTER.sh
```

2. **Configure Cursor**:
   - Settings → Features → Custom LLM
   - Base URL: `http://localhost:8001`
   - Model: `npllm`

See [Cursor Integration Guide](CURSOR_INTEGRATION.md) for details.

## Configuration

### Using API Models (Recommended for Development)

Edit `config/default.yaml`:

```yaml
model:
  mode: "api"
  provider: "groq"  # or "gemini"
```

Set environment variable:
```bash
export GROQ_API_KEY="your-api-key"
```

### Using Local Models

```yaml
model:
  mode: "local"
  base_model: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

## Troubleshooting

### PostgreSQL Connection Error

- Check if PostgreSQL is running: `docker compose ps`
- Verify connection settings in `.env`
- Check if pgvector extension is installed

### Model Loading Error

- For API models: Verify API key is set
- For local models: Ensure sufficient RAM
- Check model path in configuration

### Import Errors

- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python3 --version` (should be 3.11+)

## Next Steps

- Read [Architecture Documentation](ARCHITECTURE.md)
- Explore [API Documentation](API.md)
- Check [Implementation Plan](mvp-general-assistant/IMPLEMENTACAO-MVP.md)

