# API Streaming Documentation

## Overview

npllm API supports "fake streaming" that sends status updates via Server-Sent Events (SSE) to provide user feedback during long-running operations.

## How It Works

Instead of streaming actual tokens, the API sends status messages indicating the current stage of processing:

1. **Starting**: Query processing initiated
2. **Adapter Selection**: Selecting appropriate LoRA adapter
3. **Generating**: LLM generating response
4. **Done**: Complete response ready

## Usage

### Request with Streaming

```bash
curl -X POST "http://localhost:8000/query?stream=true" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Your question here"
  }'
```

### SSE Event Format

```
event: status
data: {"status": "starting"}

event: status
data: {"status": "adapter_selection"}

event: status
data: {"status": "generating"}

event: done
data: {"response": "Complete response text here..."}
```

## Python Example

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/query",
    params={"stream": True},
    json={"query": "Your question here"},
    stream=True
)

for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data: '):
            data = json.loads(line_str[6:])
            if 'status' in data:
                print(f"Status: {data['status']}")
            elif 'response' in data:
                print(f"Response: {data['response']}")
```

## Status Messages

- `"starting"`: Processing initiated
- `"adapter_selection"`: Selecting LoRA adapter
- `"generating"`: LLM generating response
- `"done"`: Processing complete, final response available

## Benefits

- **User Feedback**: Users know the system is working
- **Progress Indication**: Shows current processing stage
- **Non-blocking**: Doesn't wait for complete response before starting
- **Simple Implementation**: Easier than real token streaming

## Future Improvements

- [ ] Real token streaming (character by character)
- [ ] Estimated time remaining
- [ ] Processing percentage
- [ ] Error events

