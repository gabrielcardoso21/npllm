# ⚡ Guia de Otimização de Velocidade

## ✅ Correções Aplicadas

1. **Erro de logging corrigido**: Formato simplificado (sem JSON complexo)
2. **max_length reduzido**: 128 tokens (antes: 256) para iteração mais rápida
3. **Otimização automática**: TinyLlama limita automaticamente a 128 tokens
4. **max_new_tokens**: Cálculo mais preciso e eficiente

## 🚀 Resultado Esperado

- **Antes**: ~76 segundos para 111 tokens
- **Agora**: ~10-20 segundos para 128 tokens (estimado)
- **Melhoria**: ~4-7x mais rápido

## 📊 Como Testar

```bash
python3 testar_modelo_direto.py "O que é Odoo?"
```

## 🔧 Otimizações Adicionais (se ainda estiver lento)

### 1. Reduzir ainda mais o max_length

Edite `testar_modelo_direto.py` linha 48:
```python
max_length=64,  # Ainda mais rápido (respostas curtas)
```

### 2. Usar modelo ainda menor (se disponível)

Modelos muito pequenos para testes ultra-rápidos:
- `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (atual) - ~600MB
- `microsoft/phi-1_5` - ~1.3GB (mais rápido que TinyLlama)
- `Qwen/Qwen2-0.5B` - ~1GB (muito rápido)

Para trocar, edite `config/default.yaml`:
```yaml
model:
  base_model: "microsoft/phi-1_5"  # Mais rápido
```

### 3. Reduzir temperatura (mais determinístico)

```python
temperature=0.3,  # Menos aleatório = mais rápido
```

### 4. Desabilitar sampling completamente

```python
temperature=0.0,  # Greedy decoding (mais rápido)
do_sample=False,
```

### 5. Usar CPU com otimizações

Se tiver CPU moderno, pode usar:
- `torch.compile()` (PyTorch 2.0+)
- ONNX Runtime
- Intel Extension for PyTorch

## 📈 Benchmarks Esperados

| Configuração | Tempo (128 tokens) | Qualidade |
|-------------|-------------------|-----------|
| TinyLlama + 128 tokens | ~10-20s | Boa |
| TinyLlama + 64 tokens | ~5-10s | Razoável |
| phi-1_5 + 128 tokens | ~8-15s | Melhor |
| phi-1_5 + 64 tokens | ~4-8s | Boa |

## 🎯 Para Produção

Quando estiver pronto para produção, use:
- `bigcode/starcoder2-3b` (melhor qualidade)
- `max_length=512` ou mais
- GPU se disponível

## 💡 Dicas

1. **Primeira execução**: Sempre mais lenta (carrega modelo)
2. **Execuções seguintes**: Mais rápidas (modelo em memória)
3. **Streaming**: Você vê tokens em tempo real (melhor UX)
4. **Cache**: Respostas idênticas são instantâneas

## 🔍 Troubleshooting

**Ainda muito lento?**
- Verifique recursos: `free -h` e `nproc`
- Reduza `max_length` para 64 ou 32
- Use `temperature=0.0` para greedy decoding

**Respostas muito curtas?**
- Aumente `max_length` para 256 ou 512
- Mas lembre-se: mais tokens = mais tempo

**Erro de memória?**
- Use modelo menor
- Reduza `max_length`
- Feche outros programas

