#!/usr/bin/env python3
"""
Script para testar RAG (Retrieval-Augmented Generation) com curso Odoo 18
Compara resposta SEM contexto vs COM contexto do curso (RAG)
FASE 2: Teste de RAG
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import initialize_system
from src.utils.logging import get_logger

logger = get_logger("test_rag_odoo")


def main():
    """Testa RAG comparando antes e depois"""
    
    print("🔍 FASE 2: Teste de RAG (Retrieval-Augmented Generation)")
    print("=" * 70)
    print("")
    
    # Carrega variáveis de ambiente
    if Path(".env").exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    # Pergunta técnica MAIS DIFÍCIL e ESPECÍFICA sobre Odoo 18
    pergunta_tecnica = """Como implementar um modelo Odoo 18 que herda de 'account.move' e adiciona funcionalidades avançadas:

1. Campo computed 'total_discount' que calcula desconto total baseado em linhas (account.move.line) usando @api.depends
2. Campo computed 'payment_status' que determina status baseado em pagamentos parciais (account.payment)
3. Método @api.model 'create_from_invoice' que cria invoice a partir de outra com validações
4. Método @api.multi 'action_post' override que adiciona lógica customizada antes de postar
5. Constraint @api.constrains que valida se total_discount não excede 50% do total
6. Método 'get_discount_lines' que retorna apenas linhas com desconto usando domain
7. Relacionamento Many2many com 'res.partner' para múltiplos responsáveis financeiros
8. Campo related 'partner_credit_limit' que busca limite de crédito do partner relacionado
9. Método 'check_credit_limit' que valida se invoice excede limite de crédito antes de postar
10. Ordenação customizada por 'invoice_date' descendente e 'amount_total' ascendente

Forneça o código Python completo com todos os imports, decorators e implementações."""
    
    print("📝 Pergunta Técnica Avançada (FASE 2 - RAG):")
    print("-" * 70)
    print(pergunta_tecnica)
    print("-" * 70)
    print("")
    
    try:
        # Inicializa sistema
        print("1️⃣ Inicializando sistema...")
        system = initialize_system()
        print("   ✅ Sistema inicializado\n")
        
        # Busca curso existente
        courses = system.list_courses()
        if not courses:
            print("❌ Nenhum curso encontrado! Execute primeiro o treinamento.")
            sys.exit(1)
        
        course_id = courses[0]['id']
        status = system.get_course_status(course_id)
        print(f"📚 Usando curso: {courses[0]['name']} (ID: {course_id})")
        print(f"   Status: {status.get('status', 'unknown')}")
        print(f"   Conceitos aprendidos: {status.get('concepts_learned', 0)}")
        print(f"   Chunks disponíveis: {status.get('content_chunks', 0)}\n")
        
        # ==========================================
        # FASE 1: RESPOSTA SEM CONTEXTO (SEM RAG)
        # ==========================================
        print("=" * 70)
        print("🔴 FASE 1: RESPOSTA SEM CONTEXTO DO CURSO (SEM RAG)")
        print("=" * 70)
        print("")
        
        print("❓ Fazendo pergunta técnica (SEM contexto do curso/RAG)...")
        start_before = time.time()
        
        result_before = system.process_query(
            query=pergunta_tecnica,
            course_context=None  # SEM contexto do curso (sem RAG)
        )
        
        elapsed_before = time.time() - start_before
        resposta_antes = result_before.get('response', '')
        
        print(f"   ⏱️ Tempo de resposta: {elapsed_before:.2f}s")
        print(f"   📏 Tamanho da resposta: {len(resposta_antes)} caracteres")
        print("")
        print("📄 Resposta SEM RAG (sem contexto do curso):")
        print("-" * 70)
        print(resposta_antes[:500] + "..." if len(resposta_antes) > 500 else resposta_antes)
        print("-" * 70)
        print("")
        
        # Salva resposta antes
        resultado_antes = {
            "timestamp": datetime.now().isoformat(),
            "pergunta": pergunta_tecnica,
            "resposta": resposta_antes,
            "tempo": elapsed_before,
            "tamanho": len(resposta_antes),
            "adapter_used": result_before.get('adapter_used'),
            "course_context_used": False,
            "rag_enabled": False
        }
        
        with open("resposta_antes_rag.json", "w", encoding="utf-8") as f:
            json.dump(resultado_antes, f, indent=2, ensure_ascii=False)
        
        print("💾 Resposta salva em: resposta_antes_rag.json")
        print("")
        
        # ==========================================
        # FASE 2: RESPOSTA COM CONTEXTO (COM RAG)
        # ==========================================
        print("=" * 70)
        print("🟢 FASE 2: RESPOSTA COM CONTEXTO DO CURSO (COM RAG)")
        print("=" * 70)
        print("")
        
        print("❓ Fazendo a MESMA pergunta técnica (COM contexto do curso/RAG)...")
        print("   🔍 Buscando conteúdo relevante no curso...")
        start_after = time.time()
        
        result_after = system.process_query(
            query=pergunta_tecnica,
            course_context=course_id  # COM contexto do curso (RAG habilitado)
        )
        
        elapsed_after = time.time() - start_after
        resposta_depois = result_after.get('response', '')
        
        print(f"   ⏱️ Tempo de resposta: {elapsed_after:.2f}s")
        print(f"   📏 Tamanho da resposta: {len(resposta_depois)} caracteres")
        print("")
        print("📄 Resposta COM RAG (com contexto do curso):")
        print("-" * 70)
        print(resposta_depois[:500] + "..." if len(resposta_depois) > 500 else resposta_depois)
        print("-" * 70)
        print("")
        
        # Salva resposta depois
        resultado_depois = {
            "timestamp": datetime.now().isoformat(),
            "pergunta": pergunta_tecnica,
            "resposta": resposta_depois,
            "tempo": elapsed_after,
            "tamanho": len(resposta_depois),
            "adapter_used": result_after.get('adapter_used'),
            "course_context_used": True,
            "course_id": course_id,
            "rag_enabled": True
        }
        
        with open("resposta_depois_rag.json", "w", encoding="utf-8") as f:
            json.dump(resultado_depois, f, indent=2, ensure_ascii=False)
        
        print("💾 Resposta salva em: resposta_depois_rag.json")
        print("")
        
        # ==========================================
        # FASE 3: COMPARAÇÃO E ANÁLISE
        # ==========================================
        print("=" * 70)
        print("📊 FASE 3: COMPARAÇÃO E ANÁLISE (SEM RAG vs COM RAG)")
        print("=" * 70)
        print("")
        
        # Palavras-chave técnicas avançadas
        keywords_tecnica = [
            '_inherit',
            'account.move',
            '@api.depends',
            '@api.model',
            '@api.multi',
            '@api.constrains',
            'computed',
            'related',
            'Many2many',
            'account.move.line',
            'account.payment',
            'res.partner',
            'action_post',
            'create_from_invoice',
            'domain',
            '_order',
            'check_credit_limit',
            'get_discount_lines',
            'total_discount',
            'payment_status',
            'partner_credit_limit',
            'ValidationError',
            'constraint',
            'override',
            'super()'
        ]
        
        print("🔍 Análise de Palavras-Chave Técnicas Avançadas:")
        print("")
        
        keywords_antes = [kw for kw in keywords_tecnica if kw.lower() in resposta_antes.lower()]
        keywords_depois = [kw for kw in keywords_tecnica if kw.lower() in resposta_depois.lower()]
        
        print(f"   SEM RAG: {len(keywords_antes)}/{len(keywords_tecnica)} palavras-chave encontradas")
        for kw in keywords_antes:
            print(f"      ✅ {kw}")
        keywords_faltando_antes = [kw for kw in keywords_tecnica if kw not in keywords_antes]
        if keywords_faltando_antes:
            print(f"      ❌ Faltando: {', '.join(keywords_faltando_antes[:5])}{'...' if len(keywords_faltando_antes) > 5 else ''}")
        
        print("")
        print(f"   COM RAG: {len(keywords_depois)}/{len(keywords_tecnica)} palavras-chave encontradas")
        for kw in keywords_depois:
            print(f"      ✅ {kw}")
        keywords_faltando_depois = [kw for kw in keywords_tecnica if kw not in keywords_depois]
        if keywords_faltando_depois:
            print(f"      ❌ Faltando: {', '.join(keywords_faltando_depois[:5])}{'...' if len(keywords_faltando_depois) > 5 else ''}")
        
        print("")
        
        # Calcula percentuais
        percentual_antes = (len(keywords_antes) / len(keywords_tecnica)) * 100
        percentual_depois = (len(keywords_depois) / len(keywords_tecnica)) * 100
        melhoria = len(keywords_depois) - len(keywords_antes)
        
        print("📈 Melhoria com RAG:")
        if melhoria > 0:
            print(f"   ✅ +{melhoria} palavras-chave técnicas adicionadas com RAG")
            print(f"   📊 Taxa de acerto: {len(keywords_antes)}/{len(keywords_tecnica)} → {len(keywords_depois)}/{len(keywords_tecnica)}")
            print(f"   📈 Melhoria: {percentual_antes:.1f}% → {percentual_depois:.1f}% (+{percentual_depois - percentual_antes:.1f}%)")
        elif melhoria == 0:
            print(f"   ⚠️ Nenhuma melhoria detectada")
            print(f"   📊 Taxa de acerto mantida: {len(keywords_antes)}/{len(keywords_tecnica)} ({percentual_antes:.1f}%)")
        else:
            print(f"   ❌ {abs(melhoria)} palavras-chave a menos (regressão)")
            print(f"   📊 Taxa de acerto: {len(keywords_antes)}/{len(keywords_tecnica)} → {len(keywords_depois)}/{len(keywords_tecnica)}")
            print(f"   📉 Regressão: {percentual_antes:.1f}% → {percentual_depois:.1f}% ({percentual_depois - percentual_antes:.1f}%)")
        
        print("")
        print("📋 Resumo Comparativo:")
        print("-" * 70)
        print(f"   Tempo de resposta:")
        print(f"      SEM RAG: {elapsed_before:.2f}s")
        print(f"      COM RAG: {elapsed_after:.2f}s")
        print(f"      Diferença: {elapsed_after - elapsed_before:+.2f}s")
        print("")
        print(f"   Tamanho da resposta:")
        print(f"      SEM RAG: {len(resposta_antes)} caracteres")
        print(f"      COM RAG: {len(resposta_depois)} caracteres")
        print(f"      Diferença: {len(resposta_depois) - len(resposta_antes):+d} caracteres")
        print("")
        print(f"   Qualidade técnica:")
        print(f"      SEM RAG: {len(keywords_antes)}/{len(keywords_tecnica)} palavras-chave ({percentual_antes:.1f}%)")
        print(f"      COM RAG: {len(keywords_depois)}/{len(keywords_tecnica)} palavras-chave ({percentual_depois:.1f}%)")
        print(f"      Melhoria: {melhoria:+d} palavras-chave ({percentual_depois - percentual_antes:+.1f}%)")
        print("-" * 70)
        print("")
        
        # Salva comparação completa
        comparacao = {
            "fase": "FASE 2 - RAG",
            "pergunta": pergunta_tecnica,
            "sem_rag": resultado_antes,
            "com_rag": resultado_depois,
            "analise": {
                "keywords_sem_rag": keywords_antes,
                "keywords_com_rag": keywords_depois,
                "keywords_faltando_sem_rag": keywords_faltando_antes,
                "keywords_faltando_com_rag": keywords_faltando_depois,
                "melhoria_keywords": melhoria,
                "percentual_sem_rag": percentual_antes,
                "percentual_com_rag": percentual_depois,
                "melhoria_percentual": percentual_depois - percentual_antes,
                "diferenca_tempo": elapsed_after - elapsed_before,
                "diferenca_tamanho": len(resposta_depois) - len(resposta_antes)
            }
        }
        
        with open("comparacao_rag.json", "w", encoding="utf-8") as f:
            json.dump(comparacao, f, indent=2, ensure_ascii=False)
        
        print("💾 Comparação completa salva em: comparacao_rag.json")
        print("")
        
        # Conclusão
        print("=" * 70)
        if melhoria > 0 and percentual_depois >= 70:
            print("🎉 CONCLUSÃO: RAG MELHOROU a resposta!")
            print(f"   ✅ Melhoria de {melhoria} palavras-chave técnicas com RAG")
            print(f"   ✅ Taxa de acerto: {percentual_depois:.1f}%")
            print("   ✅ O sistema RAG está funcionando corretamente")
            print("   ✅ O contexto do curso está sendo utilizado efetivamente")
        elif melhoria > 0:
            print("⚠️ CONCLUSÃO: RAG melhorou, mas ainda pode melhorar mais")
            print(f"   ✅ Melhoria de {melhoria} palavras-chave técnicas")
            print(f"   ⚠️ Taxa de acerto: {percentual_depois:.1f}% (meta: 70%+)")
            print("   💡 Considere adicionar mais conteúdo relevante ao curso")
        else:
            print("❌ CONCLUSÃO: RAG não melhorou significativamente")
            print("   💡 Verifique se o conteúdo do curso é relevante para a pergunta")
            print("   💡 Considere melhorar a busca semântica ou adicionar mais conteúdo")
        print("=" * 70)
        print("")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if 'system' in locals():
            system.close()


if __name__ == "__main__":
    main()

