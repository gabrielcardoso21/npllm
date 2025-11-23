# Reference: Cursor Plugins and Extensions for Custom Models

## Overview

Cursor IDE supports integration with custom models through:
1. **MCP Servers (Model Context Protocol)** - Official recommended way
2. **OpenAI-Compatible APIs** - Via Custom LLM configuration
3. **VSCode Extensions** - Extensions that work in Cursor

## Existing Plugins/Extensions

### 1. MCP Servers for RAG

#### mcp-local-rag
- **GitHub**: https://github.com/shinpr/mcp-local-rag
- **What it does**: Local RAG server for Cursor, Claude Code and Codex
- **Features**:
  - Document ingestion (PDF, DOCX, TXT, MD)
  - Local semantic search
  - Vector database storage
  - Compatible with Cursor via MCP

#### Cursor-history-MCP
- **GitHub**: https://github.com/markelaugust74/Cursor-history-MCP
- **What it does**: Search in Cursor conversation history
- **Features**:
  - Chat history vectorization
  - Efficient search with LanceDB and Ollama
  - API to search history

#### Ragie MCP Server
- **Website**: https://www.ragie.ai
- **What it does**: MCP server that connects Cursor to external sources
- **Features**:
  - Integration with Google Drive, Jira, Slack
  - Multi-source RAG
  - Contextual search

### 2. Extensions for Custom Models

#### Ollama Integration
- **What it does**: Allows using local Ollama models in Cursor
- **How it works**: Via Custom LLM configuration with Ollama API
- **Format**: OpenAI-compatible API

#### LM Studio Integration
- **What it does**: Allows using LM Studio models in Cursor
- **How it works**: Via Custom LLM configuration
- **Format**: OpenAI-compatible API

### 3. Common Integration Patterns

#### Pattern 1: OpenAI-Compatible API
```json
{
  "cursor.customLLM": {
    "apiUrl": "http://localhost:11434/v1",  // Ollama
    "model": "llama2",
    "apiKey": ""
  }
}
```

#### Pattern 2: MCP Server
```json
{
  "mcp.servers": {
    "npllm": {
      "command": "python",
      "args": ["-m", "src.api.mcp_server"],
      "env": {}
    }
  }
}
```

## How npllm Compares

### npllm Advantages over existing plugins:

1. **Continuous Learning**:
   - ✅ npllm: Learns from feedback and consolidates during sleep
   - ❌ Others: Only static RAG

2. **Persistent Memory**:
   - ✅ npllm: PostgreSQL with persistent embeddings
   - ❌ Others: Usually in-memory or temporary

3. **Consolidated Knowledge**:
   - ✅ npllm: Incremental fine-tuning of adapters
   - ❌ Others: Only search, no learning

4. **Multi-Layer RAG**:
   - ✅ npllm: History + Courses + Consolidated Knowledge
   - ⚠️ Others: Usually only one source

### What we can learn from existing plugins:

1. **MCP Format**: We can create an MCP server for npllm
2. **OpenAI-Compatible**: Already implemented in adapter
3. **Simple Integration**: Follow established patterns

## Recommended Implementation for npllm

### Option 1: OpenAI-Compatible Adapter (ALREADY IMPLEMENTED)
✅ **Status**: Ready to use
- File: `src/api/cursor_adapter.py`
- Script: `./INICIAR_CURSOR_ADAPTER.sh`
- Port: 8001

### Option 2: MCP Server (RECOMMENDED FOR FUTURE)
📋 **Status**: Planned
- Follow official MCP pattern
- Natively compatible with Cursor
- More integrated than adapter

### Option 3: VSCode Extension
📋 **Status**: Planned
- Works in Cursor (VSCode-based)
- Graphical interface for configuration
- Easier for users

## Comparison with Existing Solutions

| Feature | mcp-local-rag | Cursor-history-MCP | npllm |
|---------|---------------|-------------------|-------|
| Local RAG | ✅ | ✅ | ✅ |
| Conversation History | ❌ | ✅ | ✅ |
| Continuous Learning | ❌ | ❌ | ✅ |
| Persistent Memory | ⚠️ | ⚠️ | ✅ |
| Fine-tuning | ❌ | ❌ | ✅ |
| Consolidation (Sleep) | ❌ | ❌ | ✅ |
| Courses/Knowledge | ❌ | ❌ | ✅ |

## Next Steps

1. ✅ **OpenAI-Compatible Adapter** - Already implemented
2. 📋 **MCP Server** - Create following official pattern
3. 📋 **VSCode Extension** - To facilitate installation
4. 📋 **Installation Documentation** - Step-by-step guide

