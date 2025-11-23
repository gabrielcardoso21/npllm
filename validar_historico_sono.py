#!/usr/bin/env python3
"""
Script para validar:
1. Se o sistema busca histórico de conversas
2. Se o sistema usa conhecimento consolidado após sono
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import initialize_system
from src.utils.logging import get_logger

logger = get_logger("validar_historico_sono")


def main():
    """Valida histórico e consolidação após sono"""
    
    print("🔍 Validação de Histórico e Consolidação (Sono)")
    print("=" * 70)
    print("")
    
    # Carrega variáveis de ambiente
    if Path(".env").exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    try:
        # Inicializa sistema
        print("1️⃣ Inicializando sistema...")
        system = initialize_system()
        print("   ✅ Sistema inicializado\n")
        
        # ==========================================
        # FASE 1: CRIAR HISTÓRICO DE CONVERSAS
        # ==========================================
        print("=" * 70)
        print("📝 FASE 1: Criando Histórico de Conversas")
        print("=" * 70)
        print("")
        
        # Cria uma sequência de conversas relacionadas
        conversas = [
            {
                "query": "Meu nome é Gabriel e estou trabalhando em um projeto Odoo 18",
                "contexto": "apresentacao"
            },
            {
                "query": "Preciso criar um módulo de biblioteca com modelos de livros",
                "contexto": "projeto_odoo"
            },
            {
                "query": "O modelo deve ter campos name, author e isbn",
                "contexto": "projeto_odoo"
            },
            {
                "query": "Quero usar Many2one para author relacionado a res.partner",
                "contexto": "projeto_odoo"
            }
        ]
        
        print(f"📚 Criando {len(conversas)} conversas relacionadas...")
        feedback_ids = []
        
        for i, conv in enumerate(conversas, 1):
            print(f"\n   {i}. Query: {conv['query'][:50]}...")
            
            result = system.process_query(
                query=conv['query'],
                project_path="/fake/project/odoo",
                file_path="/fake/project/odoo/models/library.py"
            )
            
            response = result.get('response', '')
            print(f"      Resposta: {len(response)} caracteres")
            
            # Armazena feedback (simula feedback positivo)
            try:
                # Gera embedding
                query_embedding = system.content_processor.generate_embedding(conv['query'])
                
                # Armazena feedback com score positivo
                feedback_id = system.storage.store_feedback(
                    prompt=conv['query'],
                    response=response,
                    score=0.85,  # Score positivo
                    implicit_score=0.8,
                    emotional_score=0.9,
                    context=conv['contexto'],
                    embedding=query_embedding
                )
                
                feedback_ids.append(feedback_id)
                print(f"      ✅ Feedback armazenado (ID: {feedback_id})")
                
            except Exception as e:
                print(f"      ⚠️ Erro ao armazenar feedback: {e}")
        
        print(f"\n   ✅ {len(feedback_ids)} feedbacks armazenados")
        print("")
        
        # ==========================================
        # FASE 2: VALIDAR BUSCA DE HISTÓRICO
        # ==========================================
        print("=" * 70)
        print("🔍 FASE 2: Validando Busca de Histórico")
        print("=" * 70)
        print("")
        
        # Pergunta que deve usar o histórico
        pergunta_historico = "Qual é o nome do projeto que estou trabalhando e quais campos preciso no modelo?"
        
        print(f"❓ Pergunta que requer histórico:")
        print(f"   {pergunta_historico}")
        print("")
        
        # Busca feedbacks similares (simula busca de histórico)
        print("   🔍 Buscando histórico de conversas...")
        query_embedding = system.content_processor.generate_embedding(pergunta_historico)
        
        try:
            # Busca feedbacks similares
            similar_feedbacks = system.storage.search_similar(
                query_embedding=query_embedding,
                top_k=5,
                min_score=0.7
            )
            
            print(f"   ✅ Encontrados {len(similar_feedbacks)} feedbacks similares")
            
            if similar_feedbacks:
                print("   📋 Histórico encontrado:")
                for i, fb in enumerate(similar_feedbacks[:3], 1):
                    print(f"      {i}. {fb['prompt'][:60]}...")
                    print(f"         Score: {fb.get('score', 0):.2f}, Similaridade: {fb.get('similarity', 0):.2f}")
            else:
                print("   ⚠️ Nenhum histórico encontrado")
            
        except Exception as e:
            print(f"   ❌ Erro ao buscar histórico: {e}")
            similar_feedbacks = []
        
        print("")
        
        # ==========================================
        # FASE 3: SIMULAR SONO E CONSOLIDAÇÃO
        # ==========================================
        print("=" * 70)
        print("😴 FASE 3: Simulando Sono e Consolidação")
        print("=" * 70)
        print("")
        
        print("   ⏳ Forçando inatividade (simulando 30 minutos)...")
        
        # Força inatividade modificando last_activity
        system.sleep.last_activity = datetime.utcnow() - timedelta(minutes=31)
        
        print("   ✅ Sistema marcado como inativo")
        print("")
        
        print("   🔄 Iniciando consolidação (sono)...")
        resultado_sono = system.sleep.consolidate()
        
        print(f"   Status: {resultado_sono.get('status', 'unknown')}")
        
        if resultado_sono.get('status') == 'success':
            print(f"   ✅ Consolidação concluída!")
            print(f"   📊 Feedbacks processados: {resultado_sono.get('feedbacks_processed', 0)}")
            print(f"   📊 Dataset size: {resultado_sono.get('dataset_size', 0)}")
            print(f"   🧠 Fine-tuning: {resultado_sono.get('fine_tuning', {}).get('status', 'unknown')}")
            print(f"   🔧 Adapters atualizados: {resultado_sono.get('adapters_updated', False)}")
        else:
            print(f"   ⚠️ Consolidação: {resultado_sono.get('message', 'unknown')}")
        
        print("")
        
        # ==========================================
        # FASE 4: VALIDAR USO APÓS SONO
        # ==========================================
        print("=" * 70)
        print("✅ FASE 4: Validando Uso Após Sono")
        print("=" * 70)
        print("")
        
        # Pergunta que deve usar conhecimento consolidado
        pergunta_pos_sono = "Como criar o modelo de biblioteca que discutimos antes?"
        
        print(f"❓ Pergunta após sono:")
        print(f"   {pergunta_pos_sono}")
        print("")
        
        print("   🤖 Processando query (deve usar conhecimento consolidado)...")
        result_pos_sono = system.process_query(
            query=pergunta_pos_sono,
            project_path="/fake/project/odoo"
        )
        
        resposta_pos_sono = result_pos_sono.get('response', '')
        print(f"   ✅ Resposta gerada: {len(resposta_pos_sono)} caracteres")
        print("")
        
        # Verifica se resposta menciona elementos do histórico
        elementos_historico = [
            "Gabriel",
            "biblioteca",
            "name",
            "author",
            "isbn",
            "Many2one",
            "res.partner"
        ]
        
        elementos_encontrados = [
            elem for elem in elementos_historico
            if elem.lower() in resposta_pos_sono.lower()
        ]
        
        print("   🔍 Verificando uso de conhecimento consolidado:")
        print(f"      Elementos do histórico encontrados: {len(elementos_encontrados)}/{len(elementos_historico)}")
        for elem in elementos_encontrados:
            print(f"      ✅ {elem}")
        
        elementos_faltando = [e for e in elementos_historico if e not in elementos_encontrados]
        if elementos_faltando:
            print(f"      ❌ Faltando: {', '.join(elementos_faltando)}")
        
        print("")
        
        # ==========================================
        # RESUMO E CONCLUSÃO
        # ==========================================
        print("=" * 70)
        print("📊 RESUMO E CONCLUSÃO")
        print("=" * 70)
        print("")
        
        print("📋 Resultados:")
        print(f"   • Conversas criadas: {len(conversas)}")
        print(f"   • Feedbacks armazenados: {len(feedback_ids)}")
        print(f"   • Histórico encontrado: {len(similar_feedbacks)} feedbacks similares")
        print(f"   • Consolidação (sono): {resultado_sono.get('status', 'unknown')}")
        print(f"   • Elementos do histórico na resposta: {len(elementos_encontrados)}/{len(elementos_historico)}")
        print("")
        
        # Conclusão
        if len(similar_feedbacks) > 0:
            print("   ✅ Sistema BUSCA histórico de conversas")
        else:
            print("   ⚠️ Sistema NÃO está buscando histórico (pode precisar implementação)")
        
        if resultado_sono.get('status') == 'success':
            print("   ✅ Sistema CONSOLIDA conhecimento durante sono")
        else:
            print("   ⚠️ Sistema NÃO consolidou (pode não ter dados suficientes)")
        
        if len(elementos_encontrados) >= len(elementos_historico) * 0.5:
            print("   ✅ Sistema USA conhecimento consolidado após sono")
        else:
            print("   ⚠️ Sistema pode não estar usando conhecimento consolidado efetivamente")
        
        print("")
        
        # Salva resultados
        resultados = {
            "timestamp": datetime.now().isoformat(),
            "conversas_criadas": len(conversas),
            "feedbacks_armazenados": len(feedback_ids),
            "historico_encontrado": len(similar_feedbacks),
            "consolidacao_status": resultado_sono.get('status'),
            "elementos_historico_encontrados": len(elementos_encontrados),
            "elementos_historico_total": len(elementos_historico),
            "resposta_pos_sono": resposta_pos_sono[:500] if len(resposta_pos_sono) > 500 else resposta_pos_sono
        }
        
        with open("validacao_historico_sono.json", "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        print("💾 Resultados salvos em: validacao_historico_sono.json")
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

