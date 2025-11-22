#!/bin/bash
# Script para limpar repositório removendo arquivos obsoletos

set -e

echo "=========================================="
echo "🧹 Limpeza do Repositório"
echo "=========================================="
echo ""
echo "⚠️  Este script irá remover arquivos obsoletos"
echo "    Certifique-se de ter feito commit antes!"
echo ""
read -p "Continuar? (s/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Cancelado."
    exit 1
fi

echo ""
echo "🗑️  Removendo arquivos obsoletos..."

# Documentação antiga
rm -f ACCEPT_MODEL_TERMS.md
rm -f ANALOGIA_SISTEMA_NERVOSO.md
rm -f ARQUITETURA_BIOLOGICA.md
rm -f ARQUITETURA_COMPLETA_SISTEMA_NERVOSO.md
rm -f AUTHENTICATE_HF.md
rm -f CALCULO_RECURSOS_STARCODER.md
rm -f CASOS_DE_USO_LINUX_CORPO.md
rm -f CONFIGURAR_STARCODER.md
rm -f CORPO_FISICO_APRENDIZADO.md
rm -f FINAL_STEP.md
rm -f IMPLEMENTACAO_BASICA_HOJE.md
rm -f MODELOS_ALTERNATIVOS.md
rm -f NEXT_STEPS.md
rm -f PLANO_CORPO_FISICO.md
rm -f PLANO_IMPLEMENTACAO_BASICO.md
rm -f PLANO_IMPLEMENTACAO_SISTEMA_NERVOSO.md
rm -f PLANO_PROCESSOS_PSICOLOGICOS.md
rm -f PLANO_REDESENHO.md
rm -f PROCESSOS_PSICOLOGICOS.md
rm -f QUICK_START.md
rm -f README_HUGGINGFACE.md
rm -f README_SETUP.md
rm -f SETUP_COMPLETE.md
rm -f SOLUCAO_ACESSO.md
rm -f STARCODER_CONFIGURADO.md
rm -f STATUS.md
rm -f TEST_RESULTS.md

# Documentação duplicada/intermediária
rm -f ANALISE_RECURSOS.md
rm -f CONTAINERIZACAO_ANALISE.md
rm -f IMPLEMENTACAO_COMPLETA.md
rm -f README_IMPLEMENTACAO.md
rm -f REFACTORING_STATUS.md
rm -f TESTE_REAL_README.md
rm -f TESTES_RESULTADOS.md

# Scripts antigos
rm -f check_model_access.py
rm -f example_basic_usage.py
rm -f example_complete_workflow.py
rm -f run_full_system.py
rm -f run_with_token.sh
rm -f setup_huggingface.sh
rm -f setup.sh
rm -f test_basic.py
rm -f test_docker.py
rm -f test_integration.py
rm -f test_model_loading.py
rm -f test_quick.sh

# Configurações antigas
rm -f docker-compose.dev.yml
rm -f config/default.yaml.backup

# Diretórios obsoletos (se existirem e estiverem vazios)
if [ -d "src/peripheral" ] && [ -z "$(ls -A src/peripheral)" ]; then
    rm -rf src/peripheral
fi

if [ -d "src/rag" ] && [ ! -f "src/rag/__init__.py" ]; then
    echo "⚠️  src/rag/ existe mas pode ter código. Verifique manualmente."
fi

# Remover diretórios de documentação antiga (cuidado!)
echo ""
echo "📁 Removendo diretórios de documentação antiga..."
rm -rf docs/00-executive-summary.md 2>/dev/null || true
rm -rf docs/01-neuroplasticity-processes/ 2>/dev/null || true
rm -rf docs/02-continual-learning-techniques/ 2>/dev/null || true
rm -rf docs/03-adaptive-architectures/ 2>/dev/null || true
rm -rf docs/04-memory-mechanisms/ 2>/dev/null || true
rm -rf docs/05-tool-integrations/ 2>/dev/null || true
rm -rf docs/06-knowledge-preservation/ 2>/dev/null || true
rm -rf docs/07-advanced-topics/ 2>/dev/null || true
rm -rf docs/08-guides/ 2>/dev/null || true
rm -rf docs/09-resources/ 2>/dev/null || true
rm -rf docs/api/ 2>/dev/null || true
rm -rf docs/architecture/ 2>/dev/null || true
rm -rf docs/guides/ 2>/dev/null || true
rm -rf docs/mvp-odoo-assistant/ 2>/dev/null || true
rm -rf docs/neuroplasticity-infrastructure/ 2>/dev/null || true

# Remover deployment se não estiver sendo usado
if [ -d "deployment" ] && [ ! -f "deployment/prometheus/prometheus.yml" ]; then
    echo "⚠️  deployment/ existe. Verifique se é necessário."
fi

# Remover architecture_decisions se não for necessário
if [ -d "architecture_decisions" ]; then
    echo "⚠️  architecture_decisions/ existe. Decisões já consolidadas em docs/mvp-general-assistant/"
    read -p "Remover architecture_decisions/? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf architecture_decisions/
    fi
fi

echo ""
echo "✅ Limpeza concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Revisar mudanças: git status"
echo "   2. Adicionar mudanças: git add -A"
echo "   3. Commit: git commit -m 'chore: limpar repositório removendo arquivos obsoletos'"
echo ""

