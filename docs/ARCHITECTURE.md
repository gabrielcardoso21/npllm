# npllm Architecture

## Overview

npllm is a continuously learning AI code assistant with persistent memory and adaptive learning. This document describes the complete system architecture.

## Core Components

The system consists of 6 essential components:

1. **Base LLM** - Plug-and-play LLM (not trained)
2. **Adapter Selector** - Chooses best LoRA adapter for context
3. **LoRA Adapters** - Trained during "sleep" periods
4. **PostgreSQL + pgvector** - Persistent memory with semantic search
5. **Emotional Analyzer** - Detects user sentiment from feedback
6. **Sleep System** - Consolidates knowledge during inactivity

## System Flow

### Interaction Flow

```
User Query
    ↓
Base LLM (inference only)
    ↓
Adapter Selector
    ↓
LoRA Adapter (applied)
    ↓
Final Response
    ↓
Feedback Collection → PostgreSQL
```

### Learning Flow

```
User Interactions → Feedback (positive/negative)
    ↓
PostgreSQL Storage (with embeddings)
    ↓
Sleep System (inactivity detection)
    ↓
Replay Buffer (mix old + new examples)
    ↓
Fine-tuning (incremental LoRA training)
    ↓
Adapter Update (new version)
```

## Memory Architecture

### Three-Layer Memory

1. **Short-term**: Current conversation (in-memory)
2. **Medium-term**: PostgreSQL + pgvector (persistent)
   - Conversation history
   - Feedback with embeddings
   - Course content
   - Learned concepts
3. **Long-term**: LoRA Adapters (weights)
   - Consolidated during sleep
   - Incremental fine-tuning

### RAG (Retrieval-Augmented Generation)

**Default RAG**: Conversation history
- Searches similar past conversations
- Adds context automatically to queries

**Course RAG**: Knowledge from trained courses
- Semantic search in course content
- Relevant chunks retrieved dynamically

**Consolidated RAG**: Knowledge learned during sleep
- Concepts from validated courses
- High-quality examples from replay buffer

## Learning System

### Feedback Collection

- **Emotional Feedback (30%)**: Sentiment analysis (RoBERTa)
- **Implicit Feedback (70%)**: User actions (accept, edit, delete, ignore)

### Sleep Consolidation

Triggers after 30 minutes of inactivity:
1. Extract positive feedback (score > 0.7)
2. Mix with old examples (replay buffer)
3. Fine-tune LoRA adapters incrementally
4. Update adapter versions

### Replay Buffer

- Stores important examples
- Prevents catastrophic forgetting
- Mixes old (30%) + new (70%) examples

## Course System

### Learning Process

1. **Content Collection**: Web scraping or file reading
2. **Content Processing**: Chunking + embedding generation
3. **Pattern Extraction**: LLM identifies concepts and patterns
4. **Storage**: Concepts stored in PostgreSQL

### Validation

- Automatic validation: Generate questions, answer with context, evaluate
- Manual validation: User marks as validated

## Database Schema

### Main Tables

- `feedback`: User feedback with embeddings
- `important_examples`: Examples for replay buffer
- `courses`: Course metadata
- `course_content`: Course chunks with embeddings
- `learned_concepts`: Concepts extracted from courses

## API Architecture

### Endpoints

- `POST /query` - Process query with full pipeline
- `POST /query/direct` - Direct model inference (no adapters)
- `POST /feedback` - Submit feedback
- `GET /health` - System status
- Course management endpoints

### Cursor Adapter

OpenAI-compatible adapter at `/v1/chat/completions`:
- Port 8001 (separate from main API)
- Translates OpenAI format to npllm format
- Returns OpenAI-compatible responses

## Configuration

### Model Configuration

- **Mode**: `local` or `api`
- **Provider**: `groq` or `gemini` (when mode=api)
- **Base Model**: Model name/path

### Database Configuration

- PostgreSQL connection settings
- Pool size and connection management
- pgvector extension required

## Performance Optimizations

- **Lazy Loading**: Models loaded only when needed
- **Connection Pooling**: Efficient database connections
- **Embedding Caching**: Reuse embeddings when possible
- **Batch Processing**: Process examples in batches

## Future Improvements

- [ ] Streaming responses
- [ ] Distributed training
- [ ] Multi-model support
- [ ] Advanced replay strategies
- [ ] Course marketplace

