# 🧪 Teste Local com Modelo Menor

**Objetivo**: Iterar rapidamente localmente antes de testar no Contabo.

## 📋 Configuração

### Modelo Local (Testes Rápidos)
- **Modelo**: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
- **Tamanho**: ~600MB
- **Config**: `config/default.yaml`

### Modelo Produção (Contabo)
- **Modelo**: `bigcode/starcoder2-3b`
- **Tamanho**: ~6GB
- **Config**: `config/production.yaml`

## 🚀 Como Usar

### Teste Local (Modelo Menor)
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Testar modelo diretamente
python3 -c "from src.models.base_model import CodeLlamaBaseModel; m = CodeLlamaBaseModel(); print(m.generate('Olá!', max_length=50))"

# Testar sistema completo
python3 -c "from src.main import initialize_system; s = initialize_system(); print(s.process_query('Olá!'))"

# Testar API local
python3 -m src.api.server --host 0.0.0.0 --port 8000
```

### Produção (Modelo Maior)
No Contabo, usar `config/production.yaml` ou definir variável de ambiente:
```bash
export MODEL_BASE_MODEL="bigcode/starcoder2-3b"
```

## ⚡ Vantagens do Modelo Menor

- ✅ **Carregamento rápido**: ~5-10 segundos vs ~30-60 segundos
- ✅ **Menos RAM**: ~1GB vs ~6GB
- ✅ **Iteração rápida**: Testes em segundos
- ✅ **Mesma arquitetura**: Código funciona igual

## ⚠️ Limitações

- ❌ **Qualidade menor**: Respostas menos precisas
- ❌ **Contexto menor**: Menos tokens de contexto
- ⚠️ **Apenas para testes**: Não usar em produção

