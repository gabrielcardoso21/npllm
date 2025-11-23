# npllm Features

Complete list of features and capabilities.

## Core Features

### 1. Continuous Learning

npllm learns continuously from your interactions:

- **Emotional Feedback (30%)**: Detects sentiment from user messages
- **Implicit Feedback (70%)**: Tracks user actions (accept, edit, delete, ignore)
- **Feedback Storage**: All feedback stored in PostgreSQL with embeddings
- **Automatic Consolidation**: Knowledge consolidated during "sleep" periods

### 2. Persistent Memory

Three-layer memory architecture:

- **Short-term**: Current conversation (in-memory)
- **Medium-term**: PostgreSQL + pgvector (persistent, semantic search)
- **Long-term**: LoRA Adapters (consolidated weights)

### 3. RAG (Retrieval-Augmented Generation)

Multiple RAG sources:

- **Default RAG**: Conversation history (automatic)
- **Course RAG**: Knowledge from trained courses
- **Consolidated RAG**: Knowledge learned during sleep

### 4. Sleep Consolidation

Automatic knowledge consolidation:

- Triggers after 30 minutes of inactivity
- Extracts positive feedback (score > 0.7)
- Mixes old + new examples (replay buffer)
- Fine-tunes LoRA adapters incrementally
- Updates adapter versions

### 5. Course System

Teach npllm new knowledge:

- **Content Collection**: Web scraping, file reading, or direct input
- **Content Processing**: Automatic chunking and embedding generation
- **Pattern Extraction**: LLM identifies concepts and patterns
- **Validation**: Automatic or manual validation
- **RAG Integration**: Course knowledge available for queries

## Integration Features

### API Server

- RESTful API (FastAPI)
- OpenAI-compatible endpoint for Cursor
- Streaming support (SSE)
- Health checks

### Web Interface

- Gradio-based web UI
- Query interface
- Direct model testing
- Course management

### Cursor IDE Integration

- OpenAI-compatible adapter
- Automatic RAG from history
- Persistent memory across sessions
- Continuous learning from usage

## Architecture Features

### LoRA Adapters

- Low-Rank Adaptation for efficient fine-tuning
- Multiple adapters for different contexts
- Version management (stable/experimental)
- Incremental updates during sleep

### Adapter Selector

- Automatic adapter selection based on context
- File extension detection
- Project structure analysis
- Fallback to default adapter

### Emotional Analyzer

- RoBERTa-based sentiment analysis
- Detects frustration, satisfaction, confidence
- Converts to numerical reward signal

### Replay System

- Stores important examples
- Prevents catastrophic forgetting
- Mixes old (30%) + new (70%) examples
- Prioritizes high-satisfaction examples

## Technical Features

### Model Support

- **Local Models**: Any HuggingFace model
- **API Models**: Groq, Google Gemini
- **Easy Switching**: Configuration-based model selection

### Database

- PostgreSQL with pgvector extension
- Semantic search for similarity
- Efficient connection pooling
- Optimized for low memory usage

### Performance

- Lazy loading of models
- Batch processing
- Embedding caching
- Connection pooling

## Usage Features

### Query Processing

- Automatic history retrieval
- Context-aware responses
- Course knowledge integration
- Adapter-based refinement

### Feedback Collection

- Automatic implicit feedback
- Emotional feedback detection
- Explicit feedback support
- Score calculation (0.7 * implicit + 0.3 * emotional)

### Course Management

- Create courses from URLs, files, or text
- Automatic content processing
- Concept extraction
- Validation system

## Limitations

- Fine-tuning implementation is planned (not yet fully functional)
- Local models require sufficient RAM
- API models require internet connection
- PostgreSQL required for persistent memory

## Future Features

- [ ] Distributed training
- [ ] Multi-model ensembles
- [ ] Advanced replay strategies
- [ ] Course marketplace
- [ ] Real-time streaming responses
- [ ] MCP server implementation
- [ ] VSCode extension

