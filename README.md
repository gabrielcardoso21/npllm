# npllm - Neuroplastic Large Language Model

A continuously learning AI code assistant with persistent memory and adaptive learning.

## 🎯 Overview

**npllm** is an AI code assistant that learns continuously from your interactions, maintaining persistent memory across sessions and consolidating knowledge during periods of inactivity ("sleep"). Unlike static assistants, npllm:

- ✅ **Learns continuously** from your feedback
- ✅ **Maintains persistent memory** (PostgreSQL + pgvector)
- ✅ **Consolidates knowledge** during "sleep" periods
- ✅ **Uses RAG** for conversation history and learned courses
- ✅ **Fine-tunes adapters** incrementally without forgetting

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- Docker & Docker Compose (optional, for PostgreSQL)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/gabrielkmee/npllm.git
cd npllm
```

2. **Create virtual environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL** (using Docker):
```bash
docker compose up -d postgres
```

5. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Initialize the system**:
```bash
python3 -m src.main
```

## 📚 Documentation

- **[Architecture](docs/mvp-general-assistant/ARQUITETURA-FINAL.md)** - Complete system architecture
- **[Implementation Plan](docs/mvp-general-assistant/IMPLEMENTACAO-MVP.md)** - MVP implementation details
- **[API Documentation](docs/API.md)** - REST API endpoints
- **[Cursor Integration](docs/CURSOR_INTEGRATION.md)** - How to integrate with Cursor IDE
- **[Web Interface](docs/WEB_INTERFACE.md)** - Gradio web interface guide

## 🔧 Key Features

### 1. Continuous Learning
- Learns from user feedback (emotional + implicit)
- Stores positive examples in PostgreSQL
- Consolidates knowledge during "sleep" periods

### 2. Persistent Memory
- PostgreSQL + pgvector for semantic search
- Conversation history retrieval
- Learned concepts from courses

### 3. RAG (Retrieval-Augmented Generation)
- **Default RAG**: Conversation history
- **Course RAG**: Knowledge from trained courses
- **Consolidated RAG**: Knowledge learned during sleep

### 4. Adaptive Architecture
- Base LLM (plug-and-play, not trained)
- LoRA Adapters (trained during sleep)
- Adapter Selector (chooses best adapter for context)

## 📖 Usage Examples

### Basic Query
```python
from src.main import initialize_system

system = initialize_system()
result = system.process_query("How to create an Odoo 18 model?")
print(result['response'])
```

### With Course Context
```python
# Create and train a course
course = system.create_course(
    name="Odoo 18 Development",
    description="Odoo 18 module development guide",
    source_type="url",
    source_path="https://www.odoo.com/documentation/18.0/..."
)
system.start_course_learning(course['id'])

# Query with course context
result = system.process_query(
    "How to create a Many2one field?",
    course_context=course['id']
)
```

### API Server
```bash
# Start API server
./INICIAR_API.sh

# Or use Python
python3 -m src.api
```

### Web Interface
```bash
# Start Gradio web interface
./INICIAR_WEB.sh

# Or use Python
python3 -m src.web
```

## 🔌 Integration with Cursor IDE

npllm can be integrated with Cursor IDE using an OpenAI-compatible adapter:

1. **Start the Cursor adapter**:
```bash
./INICIAR_CURSOR_ADAPTER.sh
```

2. **Configure Cursor**:
   - Base URL: `http://localhost:8001`
   - Model: `npllm`

See [Cursor Integration Guide](docs/CURSOR_INTEGRATION.md) for details.

## 🏗️ Architecture

The system consists of 6 essential components:

1. **Base LLM** - Plug-and-play LLM (not trained)
2. **Adapter Selector** - Chooses best LoRA adapter for context
3. **LoRA Adapters** - Trained during "sleep" periods
4. **PostgreSQL + pgvector** - Persistent memory with semantic search
5. **Emotional Analyzer** - Detects user sentiment from feedback
6. **Sleep System** - Consolidates knowledge during inactivity

## 📊 Project Status

- ✅ Core architecture implemented
- ✅ PostgreSQL storage with pgvector
- ✅ Course learning system
- ✅ RAG with conversation history
- ✅ Sleep consolidation system
- ✅ API server (FastAPI)
- ✅ Web interface (Gradio)
- ✅ Cursor adapter (OpenAI-compatible)
- 📋 Fine-tuning implementation (planned)

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📝 License

[Add your license here]

## 🙏 Acknowledgments

Built with inspiration from:
- Neuroplasticity concepts in AI
- RAG (Retrieval-Augmented Generation)
- LoRA (Low-Rank Adaptation)
- Replay mechanisms for continual learning
