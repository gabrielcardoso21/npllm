# Streaming Adapter Documentation

## Overview

This document details how LoRA adapters are applied during text generation, ensuring tokens are already adapted when streaming.

## How It Works

### Adapter Loading Before Generation

The adapter is loaded **before** text generation begins, so all generated tokens are already adapted:

1. **Adapter Selection**: Selector chooses appropriate LoRA adapter
2. **Adapter Loading**: Adapter is loaded onto the base model
3. **Generation**: Model generates tokens (already adapted)
4. **Streaming**: Tokens are streamed as they are generated

### Why This Approach?

- **Consistency**: All tokens come from the adapted model
- **Efficiency**: No post-processing needed
- **Real-time**: Tokens are already adapted as they're generated

## Implementation

```python
# Adapter is loaded before generation
adapter = adapter_manager.load_adapter_for_generation(context)
model = base_model.load_model()

# Apply adapter to model
model = adapter.apply(model)

# Generate with adapter already applied
for token in model.generate_stream(prompt):
    yield token  # Token is already adapted
```

## Current Status

With "fake streaming" (status updates), the adapter is still loaded before generation, but status messages are sent instead of individual tokens.

## Future: Real Streaming

When implementing real token streaming, the same approach applies:
- Adapter loaded before generation
- Tokens generated with adapter already applied
- Tokens streamed in real-time

