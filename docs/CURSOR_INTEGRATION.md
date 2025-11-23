# Cursor IDE Integration

## Overview

npllm can be integrated with Cursor IDE to provide enhanced AI assistance with continuous learning and persistent memory.

## Native Cursor RAG vs npllm

### What Cursor does natively:
- ✅ **Codebase RAG**: Automatically searches relevant code from current project
- ✅ **Open Files Context**: Uses files open in editor as context
- ✅ **Semantic Search**: Finds similar code in project
- ⚠️ **NO History RAG**: Does not search previous conversations automatically
- ⚠️ **NO Persistent Memory**: Does not learn between sessions

### What npllm adds:
- ✅ **History RAG**: Searches previous conversations automatically
- ✅ **Persistent Memory**: Knowledge persists in PostgreSQL
- ✅ **Consolidated Knowledge**: Uses knowledge learned during "sleep"
- ✅ **Continuous Learning**: Improves over time through feedback

## Integration Methods

### Method 1: OpenAI-Compatible Adapter (RECOMMENDED) ✅

npllm includes an OpenAI-compatible adapter that allows Cursor to use npllm as if it were OpenAI/Anthropic.

#### Setup

1. **Start the Cursor adapter**:
```bash
./INICIAR_CURSOR_ADAPTER.sh
```

The adapter runs on port **8001** (separate from main API on 8000).

2. **Configure Cursor**:

   **Via settings.json**:
   ```json
   {
     "cursor.customLLM": {
       "apiUrl": "http://localhost:8001/v1/chat/completions",
       "apiKey": "",
       "model": "npllm"
     }
   }
   ```

   **Via Cursor UI**:
   - Settings → Features → Custom LLM
   - Base URL: `http://localhost:8001`
   - Model: `npllm`

#### How It Works

The adapter:
1. Receives requests in OpenAI format (`/v1/chat/completions`)
2. Extracts conversation history (sent by Cursor)
3. **npllm searches additional history** in PostgreSQL (RAG of previous conversations)
4. **npllm searches consolidated knowledge** (learned during sleep)
5. Processes everything combined
6. Returns response in OpenAI format

#### Advantages

- ✅ **Compatible with Cursor**: Uses OpenAI format that Cursor understands
- ✅ **Automatic RAG**: npllm searches history automatically
- ✅ **Conversation History**: Searches previous conversations in PostgreSQL
- ✅ **Consolidated Knowledge**: Uses knowledge learned during sleep
- ✅ **Persistent Memory**: Knowledge persists between sessions

### Method 2: MCP Server (Model Context Protocol)

Cursor supports MCP servers for advanced RAG (similar to `mcp-local-rag`, `Cursor-history-MCP`). You can create an MCP server that:
- Connects to npllm
- Provides context via MCP
- Allows Cursor to search history/knowledge

**Status**: Planned for future implementation

### Method 3: VSCode Extension

Create a VSCode extension (works in Cursor) that:
- Intercepts Cursor queries
- Adds npllm context
- Sends enriched query back

**Status**: Planned for future implementation

## Comparison with Existing Plugins

| Plugin/Extension | RAG | History | Learning | Persistent Memory |
|----------------|-----|---------|----------|-------------------|
| **mcp-local-rag** | ✅ | ❌ | ❌ | ⚠️ |
| **Cursor-history-MCP** | ✅ | ✅ | ❌ | ⚠️ |
| **Ollama/LM Studio** | ❌ | ❌ | ❌ | ❌ |
| **npllm** | ✅ | ✅ | ✅ | ✅ |

**npllm Differentiator**: Continuous learning + Sleep consolidation + Incremental fine-tuning

## Installation Steps

### Step 1: Start npllm Cursor Adapter

```bash
cd npllm
./INICIAR_CURSOR_ADAPTER.sh
```

You should see:
```
🚀 npllm Cursor Adapter iniciado!
📡 Endpoint: http://localhost:8001/v1/chat/completions
💡 Configure o Cursor para usar esta URL
```

### Step 2: Configure Cursor

1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Search for "Custom LLM" or "Custom API"
3. Configure:
   - **Base URL**: `http://localhost:8001`
   - **Model**: `npllm`
   - **API Key**: (leave empty if not configured)

### Step 3: Test Integration

1. Open a chat in Cursor
2. Ask a question
3. npllm will automatically:
   - Search conversation history
   - Use consolidated knowledge
   - Return enhanced response

## How npllm Complements Cursor's Native RAG

### Integrated Flow:

1. **Cursor searches project code** (native RAG)
2. **npllm searches conversation history** (additional RAG)
3. **npllm searches consolidated knowledge** (additional RAG)
4. **npllm searches course context** (additional RAG, if available)
5. **Everything is combined** in the final query

### Example:

```python
# When Cursor asks a question:
# 1. Cursor already searches relevant code (native)
# 2. npllm adds conversation history
# 3. npllm adds consolidated knowledge
# 4. Final response uses everything combined
```

## Troubleshooting

### Adapter Not Starting

- Check if port 8001 is available: `lsof -i :8001`
- Verify dependencies: `pip install -r requirements.txt`
- Check logs for errors

### Cursor Not Connecting

- Verify adapter is running: `curl http://localhost:8001/health`
- Check Cursor settings for correct URL
- Ensure no firewall blocking port 8001

### No History Being Used

- Verify feedback has been stored in PostgreSQL
- Check if course has been trained
- Ensure sleep consolidation has run

## Advanced Configuration

### Custom Port

Edit `src/api/cursor_adapter.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=YOUR_PORT)
```

### Authentication

Add API key support in adapter if needed.

## Limitations

- Cursor does not have native support for custom APIs via UI
- Requires adapter or manual configuration
- API REST integration requires manual setup or extension

## Future Improvements

- [ ] Official MCP server implementation
- [ ] VSCode extension for easier installation
- [ ] Automatic configuration wizard
- [ ] Streaming response support

