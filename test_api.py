#!/usr/bin/env python3
"""
Script de teste para API npllm
Testa endpoints principais incluindo fake streaming
"""

import requests
import json
import sys
import time
from typing import Optional

# Configuração
API_BASE_URL = "http://161.97.123.192:8000"
TIMEOUT = 120  # 2 minutos para geração


def print_header(title: str):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_status(stage: str, message: str):
    """Imprime status formatado"""
    icons = {
        "starting": "🚀",
        "context": "📚",
        "adapter_selection": "🔍",
        "adapter_selected": "✅",
        "adapter_loading": "⏳",
        "adapter_loaded": "✅",
        "adapter_fallback": "⚠️",
        "adapter_error": "❌",
        "model_loading": "🤖",
        "generating": "⚙️",
        "processing": "🔄",
        "finalizing": "✨",
    }
    icon = icons.get(stage, "📊")
    print(f"{icon} [{stage:20s}] {message}")


def test_health():
    """Testa endpoint /health"""
    print_header("TESTE: Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("✅ API está online!")
        print(f"   Health: {data.get('health', {}).get('healthy', 'unknown')}")
        print(f"   Storage: {data.get('storage_status', 'unknown')}")
        print(f"   Courses: {data.get('courses_count', 0)}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_query_normal(query: str = "Olá! Você está funcionando?"):
    """Testa query normal (sem streaming)"""
    print_header("TESTE: Query Normal (sem streaming)")
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"query": query},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        print("✅ Resposta recebida!")
        print(f"   Adapter usado: {data.get('adapter_used', 'N/A')}")
        print(f"   Contexto do curso: {data.get('course_context_used', False)}")
        print(f"\n📝 Resposta:\n{data.get('response', 'N/A')[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_query_streaming(query: str = "Crie uma função Python para calcular fibonacci"):
    """Testa query com fake streaming (status de progresso)"""
    print_header("TESTE: Query com Fake Streaming (Status de Progresso)")
    print(f"📝 Query: {query}\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/query?stream=true",
            json={"query": query},
            stream=True,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        print("📡 Recebendo eventos SSE...\n")
        
        full_response = None
        stages_seen = []
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        event_data = json.loads(line_str[6:])  # Remove "data: "
                        
                        if event_data.get('type') == 'status':
                            stage = event_data.get('stage', 'unknown')
                            message = event_data.get('message', '')
                            print_status(stage, message)
                            stages_seen.append(stage)
                        
                        elif event_data.get('type') == 'done':
                            full_response = event_data.get('response', '')
                            adapter_used = event_data.get('adapter_used', 'N/A')
                            adapter_applied = event_data.get('adapter_applied', False)
                            
                            print("\n" + "=" * 60)
                            print("✅ Geração completa!")
                            print("=" * 60)
                            print(f"🔧 Adapter usado: {adapter_used}")
                            print(f"🔧 Adapter aplicado: {adapter_applied}")
                            print(f"\n📝 Resposta completa ({len(full_response)} chars):")
                            print("-" * 60)
                            print(full_response[:500] + ("..." if len(full_response) > 500 else ""))
                            print("-" * 60)
                            
                    except json.JSONDecodeError as e:
                        print(f"⚠️  Erro ao decodificar JSON: {e}")
                        print(f"   Linha: {line_str[:100]}")
        
        print(f"\n📊 Estágios vistos: {len(stages_seen)}")
        print(f"   {', '.join(stages_seen)}")
        
        if full_response:
            return True
        else:
            print("⚠️  Resposta completa não recebida")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_query_with_file(query: str = "Analise este arquivo", file_path: str = "main.py"):
    """Testa query com file_path para seleção de adapter"""
    print_header("TESTE: Query com file_path (seleção de adapter)")
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={
                "query": query,
                "file_path": file_path
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        print("✅ Resposta recebida!")
        print(f"   Arquivo: {file_path}")
        print(f"   Adapter selecionado: {data.get('adapter_used', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_feedback():
    """Testa endpoint de feedback"""
    print_header("TESTE: Feedback")
    try:
        response = requests.post(
            f"{API_BASE_URL}/feedback",
            json={
                "query": "Teste",
                "response": "Resposta de teste",
                "user_reaction": "positive",
                "user_action": "accept",
                "explicit_feedback": 0.8
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        print("✅ Feedback enviado!")
        print(f"   Status: {data.get('status', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_courses():
    """Testa endpoints de cursos"""
    print_header("TESTE: Cursos")
    try:
        # Lista cursos
        response = requests.get(f"{API_BASE_URL}/courses", timeout=10)
        response.raise_for_status()
        courses = response.json()
        print(f"✅ Cursos encontrados: {len(courses)}")
        for course in courses[:3]:  # Mostra até 3
            print(f"   - {course.get('name', 'N/A')} ({course.get('status', 'N/A')})")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("  TESTE COMPLETO DA API NPLLM")
    print("=" * 60)
    print(f"🌐 API URL: {API_BASE_URL}")
    print(f"⏱️  Timeout: {TIMEOUT}s")
    
    results = {}
    
    # Testes básicos
    results['health'] = test_health()
    time.sleep(1)
    
    # Testes de query
    results['query_normal'] = test_query_normal()
    time.sleep(2)
    
    results['query_streaming'] = test_query_streaming()
    time.sleep(2)
    
    results['query_file'] = test_query_with_file()
    time.sleep(1)
    
    # Testes de feedback
    results['feedback'] = test_feedback()
    time.sleep(1)
    
    # Testes de cursos
    results['courses'] = test_courses()
    
    # Resumo
    print_header("RESUMO DOS TESTES")
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {status:12s} - {test_name}")
    
    print(f"\n📊 Total: {total} | ✅ Passou: {passed} | ❌ Falhou: {failed}")
    
    if failed == 0:
        print("\n🎉 Todos os testes passaram!")
        return 0
    else:
        print(f"\n⚠️  {failed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    # Permite passar query customizada como argumento
    if len(sys.argv) > 1:
        custom_query = " ".join(sys.argv[1:])
        print(f"📝 Usando query customizada: {custom_query}\n")
        test_query_streaming(custom_query)
    else:
        sys.exit(main())

