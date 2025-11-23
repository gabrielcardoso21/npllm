# 🧪 Como Testar o Modelo Localmente

## Método 1: Script Direto (Mais Simples)

Teste o modelo diretamente, sem precisar da API ou interface web:

```bash
# Ative o ambiente virtual
source .venv/bin/activate

# Execute o script com sua pergunta
python3 testar_modelo_direto.py "Olá! Como você está?"

# Ou sem argumentos (usa pergunta padrão)
python3 testar_modelo_direto.py
```

**Exemplo:**
```bash
python3 testar_modelo_direto.py "Explique o que é Python"
```

## Método 2: Python Interativo

```bash
source .venv/bin/activate
python3
```

```python
from src.models.base_model import CodeLlamaBaseModel

# Carrega modelo (primeira vez pode demorar ~30s)
model = CodeLlamaBaseModel()

# Gera resposta
resposta = model.generate("Olá! Como você está?", max_length=256)
print(resposta)
```

## Método 3: Via API (Completo)

Se quiser testar com toda a infraestrutura (adapters, feedback, etc.):

```bash
# 1. Inicie a API
./INICIAR_API.sh

# 2. Em outro terminal, teste
curl -X POST http://localhost:8000/query/direct \
  -H "Content-Type: application/json" \
  -d '{"query": "Olá!"}'
```

## Método 4: Interface Web

```bash
# 1. Inicie a API
./INICIAR_API.sh

# 2. Em outro terminal, inicie a interface
./INICIAR_WEB.sh

# 3. Acesse http://localhost:7860
# Use o botão "⚡ Modelo Direto" para testar apenas o modelo
```

## ⚡ Dicas de Performance

- **Primeira execução**: Pode demorar ~30-40s para carregar o modelo
- **Execuções seguintes**: Muito mais rápidas (modelo já carregado)
- **max_length**: Reduza para respostas mais rápidas (padrão: 256 tokens)

## 🔧 Troubleshooting

**Erro: "ModuleNotFoundError"**
```bash
# Certifique-se de estar no diretório raiz e com venv ativado
cd /home/gabriel/npllm
source .venv/bin/activate
```

**Modelo muito lento:**
- Verifique se está usando TinyLlama (modelo pequeno)
- Reduza `max_length` para 128 ou 64
- Verifique recursos disponíveis: `free -h` e `nproc`

**Modelo não responde:**
- Verifique logs: `tail -f /tmp/npllm_api_local.log`
- Teste com pergunta simples: `python3 testar_modelo_direto.py "Olá"`

