# API Models Documentation

## Overview

npllm supports external API models (Groq, Google Gemini) for fast inference without serving local models.

## Supported Providers

### 1. Groq

- **Provider**: Groq API
- **Models**: Llama 3.1 70B, Llama 3.1 8B Instant
- **Speed**: Very fast (optimized inference)
- **Cost**: Pay-per-use

### 2. Google Gemini

- **Provider**: Google Generative AI
- **Models**: Gemini 2.0 Flash, Gemini Pro
- **Speed**: Fast
- **Cost**: Pay-per-use

## Configuration

### Environment Variables

```bash
# For Groq
export GROQ_API_KEY="your-groq-api-key"

# For Google Gemini
export GOOGLE_API_KEY="your-google-api-key"
```

### Config File

Edit `config/default.yaml`:

```yaml
model:
  mode: "api"  # "local" or "api"
  provider: "groq"  # "groq" or "gemini"
  base_model: "llama-3.1-8b-instant"  # For Groq
```

## Usage

### With Groq

```yaml
model:
  mode: "api"
  provider: "groq"
```

Set `GROQ_API_KEY` environment variable.

### With Google Gemini

```yaml
model:
  mode: "api"
  provider: "gemini"
```

Set `GOOGLE_API_KEY` environment variable.

## Automatic Detection

The system automatically detects API configuration:

1. Checks `model.mode` in config
2. If `mode: "api"`, uses `APIModel`
3. Loads appropriate provider (Groq/Gemini)

## Benefits

- **Speed**: Very fast inference (especially Groq)
- **No Local Resources**: No need to load large models
- **Scalability**: Can handle multiple concurrent requests
- **Easy Switching**: Change providers via configuration

## Limitations

- **Internet Required**: Needs connection to API
- **Cost**: Pay-per-use pricing
- **Rate Limits**: Subject to API rate limits
- **Privacy**: Queries sent to external API

## Recommended for Development

Using API models is recommended for development:
- Faster iteration (no model loading)
- Lower resource requirements
- Easy to test different models

For production, consider local models for:
- Privacy
- Cost control
- No internet dependency

