# Web Interface - npllm

Lightweight web interface using **Gradio** to interact with the npllm system.

## 🚀 Quick Start

### Option 1: Automatic Script
```bash
./INICIAR_WEB.sh [port] [api_url]
```

Example:
```bash
./INICIAR_WEB.sh 7860 http://localhost:8000
```

### Option 2: Direct Python
```bash
source .venv/bin/activate
python3 -m src.web --port=7860 --api-url=http://localhost:8000
```

### Option 3: Python Module
```bash
source .venv/bin/activate
python3 -m src.web --port 7860 --host 0.0.0.0
```

## 📋 Requirements

- Python 3.8+
- Gradio 4.44.0+ (installed via `requirements.txt`)
- npllm API running (default: `http://localhost:8000`)

## 🎯 Features

### ✅ Normal Query
- Sends question and receives complete response
- Supports project and file context
- Visual feedback of status

### 📡 Streaming (Fake)
- Shows real-time progress status
- Updates: "Selecting adapter...", "Generating response...", etc.
- Complete final response

### 📝 Feedback
- Types: positive, negative, neutral, edit, delete
- Rating 1-5
- Direct submission to API

### 💚 Health Check
- Checks API status
- Shows system information
- Course count

## 🔧 Configuration

### Default Port
- **Web Interface**: `7860`
- **API**: `8000`

### Environment Variables
```bash
export API_URL=http://localhost:8000
export WEB_PORT=7860
```

### Command Line Arguments
```bash
python3 -m src.web \
  --port=7860 \
  --host=0.0.0.0 \
  --api-url=http://localhost:8000 \
  --share  # Creates public link (ngrok)
```

## 📊 Features

### Light and Fast
- ✅ Gradio optimized for ML/LLM
- ✅ Responsive interface
- ✅ Native streaming support
- ✅ ~50MB additional RAM

### Modern Interface
- ✅ Clean and smooth theme
- ✅ Responsive layout
- ✅ Visual feedback
- ✅ Markdown support

## 🔗 API Integration

The interface connects to the existing FastAPI:

- `POST /query` - Send queries
- `POST /feedback` - Send feedback
- `GET /health` - Check health

## 🐛 Troubleshooting

### API Not Connecting
```bash
# Check if API is running
curl http://localhost:8000/health

# Start API if needed
./INICIAR_API.sh
```

### Port Already in Use
```bash
# Use another port
./INICIAR_WEB.sh 7861
```

### Import Error
```bash
# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage Examples

### Simple Query
```
Question: "Create a Python function to calculate fibonacci"
```

### Query with Context
```
Question: "How to improve this function?"
Project: /home/user/myproject
File: src/utils.py
```

### Feedback
```
Type: positive
Rating: 5
```

## 🎨 Customization

Edit `src/web/gradio_ui.py` to:
- Change theme
- Add components
- Modify layout
- Add features

## 📝 Notes

- Interface is **lightweight** (~50MB RAM)
- **Does not block** the API
- Can run on **different machine** than API
- Supports **multiple simultaneous users**

