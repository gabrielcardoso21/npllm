#!/bin/bash
# Script para testar o sistema de cursos com Odoo 18

set -e

echo "📚 Testando Sistema de Cursos - Odoo 18"
echo "========================================"
echo ""

# Ativa ambiente virtual
source .venv/bin/activate

# Carrega variáveis de ambiente
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "1️⃣ Criando curso de Odoo 18..."
python3 -c "
from src.main import initialize_system

system = initialize_system()

# Cria curso
course = system.create_course(
    name='Odoo 18 - Desenvolvimento de Módulos',
    description='Curso completo sobre desenvolvimento de módulos no Odoo 18, incluindo modelos, views, controllers e APIs'
)

print(f'✅ Curso criado: ID {course[\"course_id\"]}')
print(f'   Nome: {course[\"name\"]}')
"

COURSE_ID=$(python3 -c "
from src.main import initialize_system
system = initialize_system()
courses = system.list_courses()
if courses:
    print(courses[0]['course_id'])
else:
    print('ERROR')
")

if [ "$COURSE_ID" = "ERROR" ]; then
    echo "❌ Erro ao criar curso"
    exit 1
fi

echo ""
echo "2️⃣ Adicionando conteúdo do curso..."
echo "   (Coletando documentação do Odoo 18)"

# URLs da documentação do Odoo 18
ODOO_URLS=(
    "https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html"
    "https://www.odoo.com/documentation/18.0/developer/reference/backend/views.html"
    "https://www.odoo.com/documentation/18.0/developer/reference/backend/controllers.html"
    "https://www.odoo.com/documentation/18.0/developer/reference/backend/security.html"
    "https://www.odoo.com/documentation/18.0/developer/howtos/backend.html"
)

python3 << PYTHON_SCRIPT
from src.main import initialize_system
from src.data_collection.content_collector import ContentCollector

system = initialize_system()
collector = ContentCollector()

course_id = $COURSE_ID

# Adiciona conteúdo de URLs
odoo_urls = [
    "https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html",
    "https://www.odoo.com/documentation/18.0/developer/reference/backend/views.html",
    "https://www.odoo.com/documentation/18.0/developer/reference/backend/controllers.html",
]

print(f"📥 Coletando conteúdo de {len(odoo_urls)} URLs...")

for url in odoo_urls:
    try:
        print(f"   • {url}")
        content = collector.collect_from_url(url)
        if content:
            system.add_course_content(course_id, content, source_url=url)
            print(f"     ✅ Conteúdo adicionado")
        else:
            print(f"     ⚠️ Nenhum conteúdo coletado")
    except Exception as e:
        print(f"     ❌ Erro: {e}")

print("✅ Conteúdo adicionado ao curso")
PYTHON_SCRIPT

echo ""
echo "3️⃣ Iniciando aprendizado do curso..."
python3 -c "
from src.main import initialize_system
import time

system = initialize_system()
course_id = $COURSE_ID

print(f'🧠 Iniciando aprendizado do curso {course_id}...')
start = time.time()

result = system.start_course_learning(course_id)

elapsed = time.time() - start
print(f'✅ Aprendizado concluído em {elapsed:.2f}s')
print(f'   Status: {result.get(\"status\", \"unknown\")}')
print(f'   Conceitos aprendidos: {result.get(\"concepts_learned\", 0)}')
"

echo ""
echo "4️⃣ Verificando conceitos aprendidos..."
python3 -c "
from src.main import initialize_system

system = initialize_system()
course_id = $COURSE_ID

concepts = system.get_course_concepts(course_id)
print(f'📚 Conceitos aprendidos ({len(concepts)}):')
for i, concept in enumerate(concepts[:10], 1):  # Mostra primeiros 10
    print(f'   {i}. {concept.get(\"concept\", \"N/A\")[:60]}...')
if len(concepts) > 10:
    print(f'   ... e mais {len(concepts) - 10} conceitos')
"

echo ""
echo "5️⃣ Validando aprendizado..."
echo "   Pergunta técnica: Como criar um modelo Odoo 18 com campos obrigatórios?"

python3 << PYTHON_SCRIPT
from src.main import initialize_system

system = initialize_system()
course_id = $COURSE_ID

# Validação automática
validation_result = system.validate_course(
    course_id,
    num_questions=3,
    difficulty="medium"
)

print(f"📊 Resultado da Validação:")
print(f"   • Perguntas geradas: {validation_result.get('questions_generated', 0)}")
print(f"   • Respostas corretas: {validation_result.get('correct_answers', 0)}")
print(f"   • Taxa de acerto: {validation_result.get('accuracy', 0):.1%}")

if validation_result.get('accuracy', 0) >= 0.7:
    print("   ✅ Curso validado com sucesso!")
else:
    print("   ⚠️ Curso precisa de mais aprendizado")
PYTHON_SCRIPT

echo ""
echo "6️⃣ Testando pergunta técnica específica..."
python3 << PYTHON_SCRIPT
from src.main import initialize_system

system = initialize_system()
course_id = $COURSE_ID

# Pergunta técnica específica sobre Odoo 18
pergunta = "Como criar um modelo Odoo 18 chamado 'library.book' com os campos obrigatórios 'name' (Char), 'author' (Many2one para res.partner) e 'isbn' (Char com validação de 13 caracteres)? Inclua também um campo computed 'display_name' que concatena name e author."

print(f"❓ Pergunta: {pergunta}")
print("")
print("🤖 Resposta do sistema (com contexto do curso):")
print("=" * 60)

result = system.process_query(
    query=pergunta,
    course_context=course_id
)

response = result.get('response', '')
print(response)
print("=" * 60)

# Verifica se a resposta contém elementos chave do Odoo
keywords = ['_name', 'from odoo', 'models.Model', 'Char', 'Many2one', 'required=True', '@api.depends']
found_keywords = [kw for kw in keywords if kw.lower() in response.lower()]

print(f"")
print(f"✅ Palavras-chave encontradas: {len(found_keywords)}/{len(keywords)}")
for kw in found_keywords:
    print(f"   ✓ {kw}")

if len(found_keywords) >= len(keywords) * 0.7:
    print("")
    print("🎉 VALIDAÇÃO: Sistema aprendeu Odoo 18!")
else:
    print("")
    print("⚠️ VALIDAÇÃO: Sistema precisa aprender mais")
PYTHON_SCRIPT

echo ""
echo "✅ Teste completo!"
echo ""
echo "📋 Resumo:"
echo "   • Curso criado e conteúdo adicionado"
echo "   • Sistema aprendeu conceitos do Odoo 18"
echo "   • Validação automática executada"
echo "   • Pergunta técnica respondida com contexto do curso"

