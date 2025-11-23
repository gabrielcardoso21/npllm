#!/usr/bin/env python3
"""
Script para validar aprendizado do curso Odoo 18
Compara resposta ANTES e DEPOIS do treinamento
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

logger = get_logger("validar_aprendizado")


def main():
    """Valida aprendizado comparando antes e depois"""
    
    print("📚 Validação de Aprendizado - Odoo 18")
    print("=" * 70)
    print("")
    
    # Carrega variáveis de ambiente
    if Path(".env").exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    # Pergunta técnica para validação
    pergunta_tecnica = """Como criar um modelo Odoo 18 chamado 'library.book' com os seguintes requisitos técnicos:

1. Campo obrigatório 'name' (Char, 255 caracteres, com help text "Nome do livro")
2. Campo obrigatório 'author' (Many2one para res.partner, com string "Autor")
3. Campo 'isbn' (Char, 13 caracteres, com validação de formato ISBN-13)
4. Campo computed 'display_name' que concatena name e author.name usando @api.depends
5. Método _compute_display_name que implementa a lógica de concatenação
6. Ordenação padrão por name (ascendente)
7. Índice no campo 'isbn' para busca rápida
8. Constraint SQL que valida formato ISBN-13

Forneça o código Python completo do modelo, incluindo todos os imports necessários do Odoo 18."""
    
    print("📝 Pergunta Técnica de Validação:")
    print("-" * 70)
    print(pergunta_tecnica)
    print("-" * 70)
    print("")
    
    try:
        # Inicializa sistema
        print("1️⃣ Inicializando sistema...")
        system = initialize_system()
        print("   ✅ Sistema inicializado\n")
        
        # ==========================================
        # FASE 1: RESPOSTA ANTES DO TREINAMENTO
        # ==========================================
        print("=" * 70)
        print("🔴 FASE 1: RESPOSTA ANTES DO TREINAMENTO")
        print("=" * 70)
        print("")
        
        print("❓ Fazendo pergunta técnica (SEM contexto do curso)...")
        start_before = time.time()
        
        result_before = system.process_query(
            query=pergunta_tecnica,
            course_context=None  # SEM contexto do curso
        )
        
        elapsed_before = time.time() - start_before
        resposta_antes = result_before.get('response', '')
        
        print(f"   ⏱️ Tempo de resposta: {elapsed_before:.2f}s")
        print(f"   📏 Tamanho da resposta: {len(resposta_antes)} caracteres")
        print("")
        print("📄 Resposta ANTES do treinamento:")
        print("-" * 70)
        print(resposta_antes)
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
            "course_context_used": False
        }
        
        with open("resposta_antes_treinamento.json", "w", encoding="utf-8") as f:
            json.dump(resultado_antes, f, indent=2, ensure_ascii=False)
        
        print("💾 Resposta salva em: resposta_antes_treinamento.json")
        print("")
        
        # ==========================================
        # FASE 2: TREINAMENTO DO CURSO
        # ==========================================
        print("=" * 70)
        print("🟡 FASE 2: TREINAMENTO DO CURSO")
        print("=" * 70)
        print("")
        
        # Verifica se já existe curso
        courses = system.list_courses()
        course_id = None
        
        if courses:
            print(f"📚 Encontrado curso existente: {courses[0]['name']} (ID: {courses[0]['id']})")
            course_id = courses[0]['id']
            
            # Verifica status
            status = system.get_course_status(course_id)
            print(f"   Status: {status.get('status', 'unknown')}")
            print(f"   Conceitos aprendidos: {status.get('concepts_learned', 0)}")
            print("")
            
            if status.get('status') == 'completed':
                print("   ✅ Curso já foi treinado!")
                print("   ⏭️ Usando curso existente (para treinar novamente, delete o curso primeiro)\n")
                # Usa curso existente
            else:
                print("   ⏳ Curso não foi treinado completamente, iniciando treinamento...\n")
                course_id = None  # Força criar novo curso
        else:
            print("📚 Nenhum curso encontrado, criando novo curso...\n")
        
        if course_id is None:
            # Cria novo curso
            print("2️⃣ Criando curso de Odoo 18...")
            odoo_docs_url = "https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html"
            
            course = system.create_course(
                name="Odoo 18 - Desenvolvimento de Módulos",
                description="Curso completo sobre desenvolvimento de módulos no Odoo 18, incluindo modelos, views, controllers e APIs",
                source_type="url",
                source_path=odoo_docs_url
            )
            
            course_id = course["id"]
            print(f"   ✅ Curso criado: ID {course_id}\n")
            
            # Inicia aprendizado
            print("3️⃣ Iniciando aprendizado do curso...")
            print("   ⏳ Coletando conteúdo da documentação...")
            print("   ⏳ Processando e aprendendo conceitos...")
            print("   ⏳ Isso pode levar alguns minutos...")
            start_training = time.time()
            
            result = system.start_course_learning(course_id)
            
            elapsed_training = time.time() - start_training
            learning_result = result.get('learning', {})
            
            print(f"   ✅ Aprendizado concluído em {elapsed_training:.2f}s")
            print(f"   📄 Documentos coletados: {result.get('documents_collected', 0)}")
            print(f"   📊 Chunks armazenados: {result.get('chunks_stored', 0)}")
            print(f"   🧠 Conceitos aprendidos: {learning_result.get('concepts_learned', 0)}")
            print(f"   🔍 Padrões encontrados: {learning_result.get('patterns_found', 0)}\n")
        
        # Lista conceitos aprendidos
        print("4️⃣ Conceitos aprendidos:")
        concepts = system.get_course_concepts(course_id)
        if concepts:
            for i, concept in enumerate(concepts[:10], 1):
                concept_name = concept.get("concept_name", "N/A")
                print(f"   {i}. {concept_name}")
            if len(concepts) > 10:
                print(f"   ... e mais {len(concepts) - 10} conceitos")
        else:
            print("   ⚠️ Nenhum conceito encontrado")
        print("")
        
        # ==========================================
        # FASE 3: RESPOSTA DEPOIS DO TREINAMENTO
        # ==========================================
        print("=" * 70)
        print("🟢 FASE 3: RESPOSTA DEPOIS DO TREINAMENTO")
        print("=" * 70)
        print("")
        
        print("❓ Fazendo a MESMA pergunta técnica (COM contexto do curso)...")
        start_after = time.time()
        
        result_after = system.process_query(
            query=pergunta_tecnica,
            course_context=course_id  # COM contexto do curso
        )
        
        elapsed_after = time.time() - start_after
        resposta_depois = result_after.get('response', '')
        
        print(f"   ⏱️ Tempo de resposta: {elapsed_after:.2f}s")
        print(f"   📏 Tamanho da resposta: {len(resposta_depois)} caracteres")
        print("")
        print("📄 Resposta DEPOIS do treinamento:")
        print("-" * 70)
        print(resposta_depois)
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
            "course_id": course_id
        }
        
        with open("resposta_depois_treinamento.json", "w", encoding="utf-8") as f:
            json.dump(resultado_depois, f, indent=2, ensure_ascii=False)
        
        print("💾 Resposta salva em: resposta_depois_treinamento.json")
        print("")
        
        # ==========================================
        # FASE 4: COMPARAÇÃO E ANÁLISE
        # ==========================================
        print("=" * 70)
        print("📊 FASE 4: COMPARAÇÃO E ANÁLISE")
        print("=" * 70)
        print("")
        
        # Palavras-chave técnicas importantes
        keywords_tecnica = [
            '_name',
            'from odoo',
            'models.Model',
            'Char',
            'Many2one',
            'required=True',
            '@api.depends',
            '_compute_display_name',
            'res.partner',
            'ordering',
            '_order',
            'index=True',
            'help=',
            'string=',
            'constraint',
            '@api.constrains',
            'SQL',
            'CONSTRAINT'
        ]
        
        print("🔍 Análise de Palavras-Chave Técnicas:")
        print("")
        
        keywords_antes = [kw for kw in keywords_tecnica if kw.lower() in resposta_antes.lower()]
        keywords_depois = [kw for kw in keywords_tecnica if kw.lower() in resposta_depois.lower()]
        
        print(f"   ANTES: {len(keywords_antes)}/{len(keywords_tecnica)} palavras-chave encontradas")
        for kw in keywords_antes:
            print(f"      ✅ {kw}")
        keywords_faltando_antes = [kw for kw in keywords_tecnica if kw not in keywords_antes]
        if keywords_faltando_antes:
            print(f"      ❌ Faltando: {', '.join(keywords_faltando_antes)}")
        
        print("")
        print(f"   DEPOIS: {len(keywords_depois)}/{len(keywords_tecnica)} palavras-chave encontradas")
        for kw in keywords_depois:
            print(f"      ✅ {kw}")
        keywords_faltando_depois = [kw for kw in keywords_tecnica if kw not in keywords_depois]
        if keywords_faltando_depois:
            print(f"      ❌ Faltando: {', '.join(keywords_faltando_depois)}")
        
        print("")
        # Calcula percentuais
        percentual_antes = (len(keywords_antes) / len(keywords_tecnica)) * 100
        percentual_depois = (len(keywords_depois) / len(keywords_tecnica)) * 100
        melhoria = len(keywords_depois) - len(keywords_antes)
        
        print("📈 Melhoria:")
        if melhoria > 0:
            print(f"   ✅ +{melhoria} palavras-chave técnicas adicionadas")
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
        print(f"      ANTES: {elapsed_before:.2f}s")
        print(f"      DEPOIS: {elapsed_after:.2f}s")
        print(f"      Diferença: {elapsed_after - elapsed_before:+.2f}s")
        print("")
        print(f"   Tamanho da resposta:")
        print(f"      ANTES: {len(resposta_antes)} caracteres")
        print(f"      DEPOIS: {len(resposta_depois)} caracteres")
        print(f"      Diferença: {len(resposta_depois) - len(resposta_antes):+d} caracteres")
        print("")
        print(f"   Qualidade técnica:")
        print(f"      ANTES: {len(keywords_antes)}/{len(keywords_tecnica)} palavras-chave ({len(keywords_antes)/len(keywords_tecnica)*100:.1f}%)")
        print(f"      DEPOIS: {len(keywords_depois)}/{len(keywords_tecnica)} palavras-chave ({len(keywords_depois)/len(keywords_tecnica)*100:.1f}%)")
        print(f"      Melhoria: {melhoria:+d} palavras-chave ({percentual_depois - percentual_antes:+.1f}%)")
        print("-" * 70)
        print("")
        
        # Salva comparação completa
        comparacao = {
            "pergunta": pergunta_tecnica,
            "antes": resultado_antes,
            "depois": resultado_depois,
            "analise": {
                "keywords_antes": keywords_antes,
                "keywords_depois": keywords_depois,
                "keywords_faltando_antes": keywords_faltando_antes,
                "keywords_faltando_depois": keywords_faltando_depois,
                "melhoria_keywords": melhoria,
                "percentual_antes": percentual_antes,
                "percentual_depois": percentual_depois,
                "melhoria_percentual": percentual_depois - percentual_antes,
                "diferenca_tempo": elapsed_after - elapsed_before,
                "diferenca_tamanho": len(resposta_depois) - len(resposta_antes)
            }
        }
        
        with open("comparacao_antes_depois.json", "w", encoding="utf-8") as f:
            json.dump(comparacao, f, indent=2, ensure_ascii=False)
        
        print("💾 Comparação completa salva em: comparacao_antes_depois.json")
        print("")
        
        # Conclusão
        print("=" * 70)
        if melhoria > 0 and percentual_depois >= 70:
            print("🎉 CONCLUSÃO: Sistema APRENDEU com o curso!")
            print(f"   ✅ Melhoria de {melhoria} palavras-chave técnicas")
            print(f"   ✅ Taxa de acerto: {percentual_depois:.1f}%")
            print("   ✅ O modelo auxiliar está funcionando corretamente")
        elif melhoria > 0:
            print("⚠️ CONCLUSÃO: Sistema melhorou, mas ainda precisa aprender mais")
            print(f"   ✅ Melhoria de {melhoria} palavras-chave técnicas")
            print(f"   ⚠️ Taxa de acerto: {percentual_depois:.1f}% (meta: 70%+)")
            print("   💡 Considere adicionar mais conteúdo ao curso")
        else:
            print("❌ CONCLUSÃO: Sistema não melhorou significativamente")
            print("   💡 Verifique se o curso foi treinado corretamente")
            print("   💡 Considere adicionar mais conteúdo relevante")
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

