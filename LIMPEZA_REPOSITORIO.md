# 🧹 Plano de Limpeza do Repositório

**Data**: 2025-01-27  
**Objetivo**: Remover tudo que não está na arquitetura simplificada

---

## ✅ O Que Manter

### Código Fonte
- `src/` - Código da arquitetura simplificada
  - `src/models/` - LLM Base
  - `src/adapters/` - LoRA Adapters + Seletor
  - `src/storage/` - PostgreSQL
  - `src/feedback/` - Análise Emocional + Implícito
  - `src/learning/` - Sono + Replay + Fine-tuning
  - `src/analysis/` - Análise Arquitetural
  - `src/patterns/` - Identificação de Padrões
  - `src/transfer/` - Transfer Learning
  - `src/generation/` - Geração Arquitetural
  - `src/utils/` - Utilitários
  - `src/main.py` - Sistema principal

### Testes
- `tests/` - Todos os testes

### Documentação Essencial
- `docs/mvp-general-assistant/` - Arquitetura final
- `README.md` - Documentação principal
- `DOCKER_QUICKSTART.md` - Setup Docker
- `SETUP_DOCKER.md` - Setup detalhado

### Configuração
- `docker-compose.yml` - PostgreSQL
- `requirements.txt` - Dependências
- `pytest.ini` - Configuração testes
- `.gitignore` - Ignorar modelos

### Scripts Essenciais
- `test_real.py` - Teste real
- `INICIAR_DOCKER.sh` - Iniciar Docker
- `EXECUTAR_TESTE_REAL.sh` - Executar teste
- `VERIFICAR_RECURSOS.py` - Verificar recursos

---

## ❌ O Que Remover

### Documentação Antiga/Obsoleta
- `ACCEPT_MODEL_TERMS.md`
- `ANALOGIA_SISTEMA_NERVOSO.md`
- `ARQUITETURA_BIOLOGICA.md`
- `ARQUITETURA_COMPLETA_SISTEMA_NERVOSO.md`
- `AUTHENTICATE_HF.md`
- `CALCULO_RECURSOS_STARCODER.md`
- `CASOS_DE_USO_LINUX_CORPO.md`
- `CONFIGURAR_STARCODER.md`
- `CORPO_FISICO_APRENDIZADO.md`
- `FINAL_STEP.md`
- `IMPLEMENTACAO_BASICA_HOJE.md`
- `MODELOS_ALTERNATIVOS.md`
- `NEXT_STEPS.md`
- `PLANO_CORPO_FISICO.md`
- `PLANO_IMPLEMENTACAO_BASICO.md`
- `PLANO_IMPLEMENTACAO_SISTEMA_NERVOSO.md`
- `PLANO_PROCESSOS_PSICOLOGICOS.md`
- `PLANO_REDESENHO.md`
- `PROCESSOS_PSICOLOGICOS.md`
- `QUICK_START.md`
- `README_HUGGINGFACE.md`
- `README_SETUP.md`
- `SETUP_COMPLETE.md`
- `SOLUCAO_ACESSO.md`
- `STARCODER_CONFIGURADO.md`
- `STATUS.md`
- `TEST_RESULTS.md`

### Documentação Duplicada/Intermediária
- `ANALISE_RECURSOS.md` (manter apenas RECURSOS_RESUMO.md)
- `CONTAINERIZACAO_ANALISE.md` (info já em SETUP_DOCKER.md)
- `IMPLEMENTACAO_COMPLETA.md` (info já em docs/mvp-general-assistant/)
- `README_IMPLEMENTACAO.md` (info já em README.md)
- `REFACTORING_STATUS.md` (histórico, não necessário)
- `TESTE_REAL_README.md` (info já em DOCKER_QUICKSTART.md)
- `TESTES_RESULTADOS.md` (histórico, não necessário)

### Diretórios de Documentação Antiga
- `docs/00-executive-summary.md`
- `docs/01-neuroplasticity-processes/`
- `docs/02-continual-learning-techniques/`
- `docs/03-adaptive-architectures/`
- `docs/04-memory-mechanisms/`
- `docs/05-tool-integrations/`
- `docs/06-knowledge-preservation/`
- `docs/07-advanced-topics/`
- `docs/08-guides/`
- `docs/09-resources/`
- `docs/api/`
- `docs/architecture/`
- `docs/architecture-decisions/` (manter apenas se relevante)
- `docs/guides/`
- `docs/mvp-odoo-assistant/` (não é mais foco)
- `docs/neuroplasticity-infrastructure/` (info já consolidada)

### Código Obsoleto
- `src/peripheral/` - Não usado na arquitetura simplificada
- `src/rag/` - Substituído por `src/storage/` (PostgreSQL direto)

### Scripts Antigos
- `check_model_access.py`
- `example_basic_usage.py`
- `example_complete_workflow.py`
- `run_full_system.py`
- `run_with_token.sh`
- `setup_huggingface.sh`
- `setup.sh` (substituído por INICIAR_DOCKER.sh)
- `test_basic.py`
- `test_docker.py`
- `test_integration.py`
- `test_model_loading.py`
- `test_quick.sh`

### Configurações Antigas
- `docker-compose.dev.yml` (não usado)
- `docker-compose.full.yml` (opcional, manter se quiser)
- `config/default.yaml.backup`
- `deployment/` (não usado na arquitetura simplificada)

### Diretórios de Decisões Antigas
- `architecture_decisions/` - Decisões antigas, já consolidadas

### Outros
- `adapters/` (se for diretório vazio ou antigo)
- `data/` (dados de teste, não necessário no repo)
- `logs/` (logs, não devem estar no repo)
- `models/` (modelos, já no .gitignore mas remover se existir)

---

## 📋 Checklist de Limpeza

- [ ] Fazer commit do estado atual
- [ ] Atualizar .gitignore
- [ ] Remover documentação antiga
- [ ] Remover código obsoleto
- [ ] Remover scripts antigos
- [ ] Remover configurações antigas
- [ ] Atualizar README.md
- [ ] Criar CHANGELOG.md documentando limpeza
- [ ] Fazer commit final

---

**Última Atualização**: 2025-01-27

