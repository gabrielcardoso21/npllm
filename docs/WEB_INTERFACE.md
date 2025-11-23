# 🌐 Interface Web - NPLLM

Interface web leve usando **Gradio** para interagir com o sistema NPLLM.

## 🚀 Início Rápido

### Opção 1: Script Automático
```bash
./INICIAR_WEB.sh [porta] [api_url]
```

Exemplo:
```bash
./INICIAR_WEB.sh 7860 http://localhost:8000
```

### Opção 2: Python Direto
```bash
source .venv/bin/activate
python3 -m src.web --port=7860 --api-url=http://localhost:8000
```

### Opção 3: Python Module
```bash
source .venv/bin/activate
python3 -m src.web --port 7860 --host 0.0.0.0
```

## 📋 Requisitos

- Python 3.8+
- Gradio 4.44.0+ (instalado via `requirements.txt`)
- API NPLLM rodando (padrão: `http://localhost:8000`)

## 🎯 Funcionalidades

### ✅ Query Normal
- Envia pergunta e recebe resposta completa
- Suporta contexto de projeto e arquivo
- Feedback visual do status

### 📡 Streaming (Fake)
- Mostra status de progresso em tempo real
- Atualizações: "Selecionando adapter...", "Gerando resposta...", etc.
- Resposta final completa

### 📝 Feedback
- Tipos: positive, negative, neutral, edit, delete
- Nota de 1-5
- Envio direto para API

### 💚 Health Check
- Verifica status da API
- Mostra informações do sistema
- Contagem de cursos

## 🔧 Configuração

### Porta Padrão
- **Interface Web**: `7860`
- **API**: `8000`

### Variáveis de Ambiente
```bash
export API_URL=http://localhost:8000
export WEB_PORT=7860
```

### Argumentos de Linha de Comando
```bash
python3 -m src.web \
  --port=7860 \
  --host=0.0.0.0 \
  --api-url=http://localhost:8000 \
  --share  # Cria link público (ngrok)
```

## 📊 Recursos

### Leve e Rápido
- ✅ Gradio é otimizado para ML/LLM
- ✅ Interface responsiva
- ✅ Suporte nativo a streaming
- ✅ ~50MB de RAM adicional

### Interface Moderna
- ✅ Tema suave e limpo
- ✅ Layout responsivo
- ✅ Feedback visual
- ✅ Suporte a markdown

## 🔗 Integração com API

A interface se conecta à API FastAPI existente:

- `POST /query` - Enviar queries
- `POST /feedback` - Enviar feedback
- `GET /health` - Verificar saúde

## 🐛 Troubleshooting

### API não conecta
```bash
# Verificar se API está rodando
curl http://localhost:8000/health

# Iniciar API se necessário
./INICIAR_API.sh
```

### Porta já em uso
```bash
# Usar outra porta
./INICIAR_WEB.sh 7861
```

### Erro de importação
```bash
# Instalar dependências
pip install -r requirements.txt
```

## 📖 Exemplos de Uso

### Query Simples
```
Pergunta: "Crie uma função Python para calcular fibonacci"
```

### Query com Contexto
```
Pergunta: "Como melhorar esta função?"
Projeto: /home/user/myproject
Arquivo: src/utils.py
```

### Feedback
```
Tipo: positive
Nota: 5
```

## 🎨 Personalização

Edite `src/web/gradio_ui.py` para:
- Mudar tema
- Adicionar componentes
- Modificar layout
- Adicionar funcionalidades

## 📝 Notas

- Interface é **leve** (~50MB RAM)
- **Não bloqueia** a API
- Pode rodar em **máquina diferente** da API
- Suporta **múltiplos usuários** simultâneos

