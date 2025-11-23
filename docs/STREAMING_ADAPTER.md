# 🔄 Streaming com Adapter LoRA

## 📋 Problema Resolvido

**Problema original**: No streaming, tokens são enviados um por um, mas o adapter LoRA precisa da resposta completa para revisar.

**Solução implementada**: O adapter LoRA é carregado no modelo base **ANTES** da geração, então os tokens já vêm "adaptados" durante o streaming.

## 🏗️ Arquitetura

### Fluxo de Streaming com Adapter

```
1. Seleciona adapter baseado no contexto
2. Carrega adapter no modelo base (PEFT)
3. Gera tokens com streaming (já adaptados)
4. Envia tokens em tempo real
5. Finaliza com resposta completa
```

### Como Funciona

1. **Seleção de Adapter**: O sistema seleciona o adapter apropriado (ex: `python_adapter`, `odoo_adapter`)

2. **Carregamento**: O adapter é carregado no modelo base usando `PeftModel.from_pretrained()`
   - Isso modifica os pesos do modelo para incluir os pesos do adapter
   - A geração subsequente já usa o adapter

3. **Geração com Streaming**: 
   - Tokens são gerados um por um
   - Cada token já está "adaptado" porque o adapter está carregado
   - Não precisa esperar resposta completa

4. **Envio em Tempo Real**: Tokens são enviados via SSE conforme são gerados

## 📡 Formato SSE

```
data: {"type": "start", "adapter": "loading"}
data: {"type": "adapter", "adapter": "python_adapter"}
data: {"type": "adapter_loaded", "adapter": "python_adapter"}
data: {"type": "token", "token": "def"}
data: {"type": "token", "token": " fibonacci"}
...
data: {"type": "done", "response": "...", "adapter_used": "python_adapter", "adapter_applied": true}
```

## ⚡ Vantagens

1. **Feedback Imediato**: Tokens aparecem em tempo real
2. **Adapter Aplicado**: Resposta já vem adaptada, não precisa revisão posterior
3. **Eficiência**: Adapter carregado uma vez, usado em todas as gerações
4. **Sem Perda de Qualidade**: Adapter é aplicado durante geração, não depois

## 🔧 Implementação Técnica

### Carregamento do Adapter

```python
# Em src/api/server.py
adapter = system.adapter_manager.get_adapter(adapter_name, prefer_stable=True)
if adapter:
    system.adapter_manager.load_adapter_for_generation(
        adapter_name, 
        system.base_model
    )
```

### Geração com Adapter Carregado

```python
# Modelo base já tem adapter carregado via PEFT
generator = system.base_model.generate(query_text, max_length=512, stream=True)

# Tokens já vêm adaptados
for token in generator:
    yield token
```

## 📝 Notas Importantes

1. **Carregamento Único**: Adapter é carregado uma vez e reutilizado
2. **Cache**: Adapters carregados ficam em cache (`_loaded_adapters`)
3. **Fallback**: Se adapter não existe, usa modelo base sem adapter
4. **Performance**: Carregar adapter tem custo, mas é feito uma vez

## 🚀 Uso

```bash
curl -N -X POST "http://161.97.123.192:8000/query?stream=true" \
  -H "Content-Type: application/json" \
  -d '{"query": "Crie uma função Python", "file_path": "main.py"}'
```

O sistema automaticamente:
1. Seleciona adapter baseado em `file_path` (ex: `.py` → `python_adapter`)
2. Carrega adapter no modelo
3. Gera resposta com streaming (já adaptada)
4. Envia tokens em tempo real

