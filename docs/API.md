# npllm API Documentation

REST API for interacting with npllm system.

## Base URL

- Local development: `http://localhost:8000`
- Production: Configure according to your deployment

## Authentication

Currently no authentication required. For production, add API key authentication.

## Endpoints

### Health Check

**GET** `/health`

Check system health status.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Process Query

**POST** `/query`

Process a user query with full pipeline (RAG, adapters, etc.).

**Request Body**:
```json
{
  "query": "How to create an Odoo 18 model?",
  "project_path": "/path/to/project",
  "file_path": "/path/to/file.py",
  "course_context": 1
}
```

**Parameters**:
- `query` (required): User question
- `project_path` (optional): Project path for context
- `file_path` (optional): File path for context
- `course_context` (optional): Course ID for RAG context
- `stream` (optional): Enable streaming (default: false)

**Response**:
```json
{
  "response": "Here's how to create an Odoo 18 model...",
  "adapter_used": "python",
  "course_context_used": true,
  "history_used": true
}
```

### Direct Query

**POST** `/query/direct`

Direct model inference without adapters or extra processing.

**Request Body**:
```json
{
  "query": "Your question here"
}
```

**Response**:
```json
{
  "response": "Direct model response..."
}
```

### Submit Feedback

**POST** `/feedback`

Submit feedback for a query/response pair.

**Request Body**:
```json
{
  "query": "Original query",
  "response": "Generated response",
  "explicit_feedback": 0.9
}
```

**Response**:
```json
{
  "status": "success",
  "feedback_id": 123
}
```

### Course Management

#### List Courses

**GET** `/courses`

List all courses.

**Response**:
```json
[
  {
    "id": 1,
    "name": "Odoo 18 Development",
    "status": "completed",
    "concepts_learned": 90
  }
]
```

#### Create Course

**POST** `/courses`

Create a new course.

**Request Body**:
```json
{
  "name": "Python Best Practices",
  "description": "Learn Python best practices",
  "source_type": "url",
  "source_path": "https://docs.python.org/3/tutorial/"
}
```

#### Start Course Learning

**POST** `/courses/{course_id}/start`

Start learning from a course.

**Response**:
```json
{
  "status": "success",
  "concepts_learned": 50,
  "chunks_stored": 323
}
```

#### Validate Course

**POST** `/courses/{course_id}/validate`

Validate a course (automatic or manual).

**Request Body**:
```json
{
  "automatic": true,
  "num_questions": 10,
  "threshold": 0.75
}
```

## Streaming (Server-Sent Events)

When `stream=true` in query, responses use Server-Sent Events (SSE):

```
event: status
data: {"status": "starting"}

event: status
data: {"status": "generating"}

event: done
data: {"response": "Full response text..."}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Status Codes**:
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## Examples

### Python

```python
import requests

# Process query
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "How to create a Python class?",
        "course_context": 1
    }
)
print(response.json()["response"])

# Submit feedback
requests.post(
    "http://localhost:8000/feedback",
    json={
        "query": "How to create a Python class?",
        "response": "Here's how...",
        "explicit_feedback": 0.9
    }
)
```

### cURL

```bash
# Process query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How to create a Python class?"}'

# Health check
curl http://localhost:8000/health
```

## Rate Limiting

Currently no rate limiting. For production, implement rate limiting based on API key or user.

## Cursor Adapter

For Cursor IDE integration, use the Cursor adapter endpoint:

- **Endpoint**: `http://localhost:8001/v1/chat/completions`
- **Format**: OpenAI-compatible
- See [Cursor Integration Guide](CURSOR_INTEGRATION_EN.md) for details

