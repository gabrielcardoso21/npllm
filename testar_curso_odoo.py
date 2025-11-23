#!/usr/bin/env python3
"""
Script para testar o sistema de cursos com Odoo 18
Cria curso, aprende e valida com pergunta técnica
"""

import os
import sys
import time
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import initialize_system
from src.utils.logging import get_logger

logger = get_logger("test_curso_odoo")


def main():
    """Testa sistema de cursos com Odoo 18"""
    
    print("📚 Testando Sistema de Cursos - Odoo 18")
    print("=" * 60)
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
        
        # Cria curso de Odoo 18
        print("2️⃣ Criando curso de Odoo 18...")
        print("   📝 Nome: Odoo 18 - Desenvolvimento de Módulos")
        print("   📖 Descrição: Curso completo sobre desenvolvimento de módulos no Odoo 18")
        print("   🔗 Fonte: Documentação oficial do Odoo 18")
        
        # URLs da documentação do Odoo 18
        odoo_docs_url = "https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html"
        
        course = system.create_course(
            name="Odoo 18 - Desenvolvimento de Módulos",
            description="Curso completo sobre desenvolvimento de módulos no Odoo 18, incluindo modelos, views, controllers e APIs",
            source_type="url",
            source_path=odoo_docs_url
        )
        
        course_id = course["id"]
        print(f"   ✅ Curso criado: ID {course_id}\n")
        
        # Inicia aprendizado (coleta conteúdo, processa e aprende)
        print("3️⃣ Iniciando aprendizado do curso...")
        print("   ⏳ Coletando conteúdo da documentação...")
        print("   ⏳ Processando e aprendendo conceitos...")
        print("   ⏳ Isso pode levar alguns minutos...")
        start_time = time.time()
        
        result = system.start_course_learning(course_id)
        
        elapsed = time.time() - start_time
        learning_result = result.get('learning', {})
        print(f"   ✅ Aprendizado concluído em {elapsed:.2f}s")
        print(f"   📄 Documentos coletados: {result.get('documents_collected', 0)}")
        print(f"   📊 Chunks armazenados: {result.get('chunks_stored', 0)}")
        print(f"   🧠 Conceitos aprendidos: {learning_result.get('concepts_learned', 0)}")
        print(f"   🔍 Padrões encontrados: {learning_result.get('patterns_found', 0)}\n")
        
        # Lista conceitos aprendidos
        print("4️⃣ Conceitos aprendidos:")
        concepts = system.get_course_concepts(course_id)
        if concepts:
            for i, concept in enumerate(concepts[:10], 1):  # Mostra primeiros 10
                concept_name = concept.get("concept_name", "N/A")
                print(f"   {i}. {concept_name}")
            if len(concepts) > 10:
                print(f"   ... e mais {len(concepts) - 10} conceitos")
        else:
            print("   ⚠️ Nenhum conceito encontrado")
        print("")
        
        # Validação automática
        print("5️⃣ Validação automática do aprendizado...")
        print("   ⏳ Gerando perguntas e validando respostas...")
        try:
            validation_result = system.validate_course(
                course_id,
                automatic=True,
                num_questions=5,  # 5 perguntas para teste rápido
                validation_threshold=0.7
            )
            
            print(f"   📊 Perguntas geradas: {validation_result.get('num_questions', 0)}")
            print(f"   📈 Score médio: {validation_result.get('average_score', 0):.2%}")
            print(f"   🎯 Threshold: {validation_result.get('validation_threshold', 0):.2%}")
            
            if validation_result.get('passed', False):
                print("   🎉 VALIDAÇÃO: Curso passou na validação automática!")
            else:
                print("   ⚠️ VALIDAÇÃO: Curso não passou (pode precisar de mais conteúdo)")
        except Exception as e:
            print(f"   ⚠️ Erro na validação automática: {e}")
            print("   💡 Continuando com validação manual...")
        print("")
        
        # Pergunta técnica específica
        print("6️⃣ Testando pergunta técnica específica...")
        print("   " + "=" * 56)
        
        pergunta = """Como criar um modelo Odoo 18 chamado 'library.book' com os seguintes requisitos:
1. Campo obrigatório 'name' (Char, 255 caracteres)
2. Campo obrigatório 'author' (Many2one para res.partner)
3. Campo 'isbn' (Char, 13 caracteres, com validação de formato ISBN)
4. Campo computed 'display_name' que concatena name e author.name
5. Método _compute_display_name usando @api.depends
6. Ordenação padrão por name

Forneça o código Python completo do modelo."""
        
        print(f"   ❓ Pergunta:")
        print(f"   {pergunta}")
        print("")
        print("   🤖 Resposta do sistema (com contexto do curso):")
        print("   " + "=" * 56)
        
        result = system.process_query(
            query=pergunta,
            course_context=course_id
        )
        
        response = result.get('response', '')
        print(f"   {response}")
        print("   " + "=" * 56)
        print("")
        
        # Validação da resposta
        print("7️⃣ Validando resposta técnica...")
        keywords_required = [
            '_name',
            'from odoo',
            'models.Model',
            'Char',
            'Many2one',
            'required=True',
            '@api.depends',
            '_compute_display_name',
            'res.partner',
            'ordering'
        ]
        
        found_keywords = [kw for kw in keywords_required if kw.lower() in response.lower()]
        missing_keywords = [kw for kw in keywords_required if kw.lower() not in response.lower()]
        
        print(f"   📋 Palavras-chave encontradas: {len(found_keywords)}/{len(keywords_required)}")
        for kw in found_keywords:
            print(f"      ✅ {kw}")
        if missing_keywords:
            print(f"   ⚠️ Palavras-chave faltando:")
            for kw in missing_keywords:
                print(f"      ❌ {kw}")
        
        accuracy = len(found_keywords) / len(keywords_required)
        print(f"   📊 Taxa de acerto: {accuracy:.1%}")
        
        if accuracy >= 0.7:
            print("")
            print("   🎉 VALIDAÇÃO FINAL: Sistema aprendeu Odoo 18!")
            print("   ✅ O modelo auxiliar está pronto para ajudar com desenvolvimento Odoo 18")
        else:
            print("")
            print("   ⚠️ VALIDAÇÃO FINAL: Sistema precisa aprender mais")
            print("   💡 Considere adicionar mais conteúdo ao curso")
        
        print("")
        print("=" * 60)
        print("✅ Teste completo!")
        print("")
        print("📋 Resumo:")
        print(f"   • Curso ID: {course_id}")
        print(f"   • Conceitos aprendidos: {len(concepts)}")
        print(f"   • Validação automática: {'✅ Passou' if validation_result.get('passed') else '❌ Não passou'}")
        print(f"   • Validação técnica: {'✅ Passou' if accuracy >= 0.7 else '❌ Não passou'}")
        
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

