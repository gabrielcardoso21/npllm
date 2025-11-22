#!/usr/bin/env python3
"""
Teste Real do Sistema npllm
Executa o sistema completo com componentes reais
"""

import sys
import time
from pathlib import Path
from src.main import NpllmSystem
from src.feedback.implicit import UserAction


def test_basic_query():
    """Teste básico: query simples"""
    print("\n" + "="*60)
    print("TESTE 1: Query Básica")
    print("="*60)
    
    try:
        system = NpllmSystem()
        print("✅ Sistema inicializado")
        
        # Query simples
        query = "Create a Python function that returns 'Hello, World!'"
        print(f"\n📝 Query: {query}")
        
        result = system.process_query(
            query=query,
            file_path="test.py"
        )
        
        print(f"\n✅ Resposta recebida:")
        print(f"   Adapter usado: {result.get('adapter_used', 'N/A')}")
        print(f"   Resposta: {result.get('response', 'N/A')[:200]}...")
        
        return system, result
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def test_feedback_capture(system, result):
    """Teste de captura de feedback"""
    print("\n" + "="*60)
    print("TESTE 2: Captura de Feedback")
    print("="*60)
    
    if not system or not result:
        print("⚠️  Pulando teste - sistema não inicializado")
        return
    
    try:
        # Simula feedback positivo
        print("\n📝 Capturando feedback positivo...")
        
        system.capture_feedback(
            query="Create a Python function that returns 'Hello, World!'",
            response=result.get('response', ''),
            user_reaction="Perfect! This is exactly what I needed.",
            user_action=UserAction.ACCEPT,
            explicit_feedback=0.9
        )
        
        print("✅ Feedback capturado e armazenado")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def test_project_analysis(system):
    """Teste de análise de projeto"""
    print("\n" + "="*60)
    print("TESTE 3: Análise de Projeto")
    print("="*60)
    
    if not system:
        print("⚠️  Pulando teste - sistema não inicializado")
        return
    
    try:
        # Cria projeto de teste temporário
        test_project = Path("/tmp/npllm_test_project")
        test_project.mkdir(exist_ok=True)
        
        # Cria estrutura simples
        (test_project / "src").mkdir(exist_ok=True)
        (test_project / "src" / "models").mkdir(exist_ok=True)
        
        # Cria arquivo de exemplo
        example_file = test_project / "src" / "models" / "user.py"
        example_file.write_text("""
class UserRepository:
    def __init__(self, db):
        self.db = db
    
    def find_by_id(self, id):
        return self.db.query(User).filter_by(id=id).first()
""")
        
        print(f"\n📁 Projeto de teste: {test_project}")
        
        # Analisa projeto
        analysis = system.analyze_project(str(test_project))
        
        print("\n✅ Análise concluída:")
        print(f"   Estrutura: {list(analysis.get('structure', {}).keys())}")
        print(f"   Padrões encontrados: {len(analysis.get('patterns_found', []))}")
        print(f"   Decisões arquiteturais: {len(analysis.get('architectural_decisions', []))}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def test_sleep_consolidation(system):
    """Teste de consolidação (sono)"""
    print("\n" + "="*60)
    print("TESTE 4: Consolidação (Sono)")
    print("="*60)
    
    if not system:
        print("⚠️  Pulando teste - sistema não inicializado")
        return
    
    try:
        print("\n⏰ Simulando inatividade...")
        
        # Simula inatividade (30 minutos)
        from datetime import datetime, timedelta
        system.sleep.last_activity = datetime.utcnow() - timedelta(minutes=31)
        
        print("🛌 Acionando consolidação...")
        
        # Aciona sono manualmente (force=True para garantir execução)
        result = system.trigger_sleep(force=True)
        
        if result:
            print("\n✅ Consolidação concluída:")
            print(f"   Status: {result.get('status', 'N/A')}")
            print(f"   Contextos treinados: {result.get('contexts_trained', 0)}")
            print(f"   Adapters atualizados: {result.get('adapters_updated', 0)}")
        else:
            print("⚠️  Nenhum feedback para consolidar")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def test_system_status(system):
    """Teste de status do sistema"""
    print("\n" + "="*60)
    print("TESTE 5: Status do Sistema")
    print("="*60)
    
    if not system:
        print("⚠️  Pulando teste - sistema não inicializado")
        return
    
    try:
        status = system.get_system_status()
        
        print("\n✅ Status do sistema:")
        print(f"   Saúde: {status.get('health', {}).get('healthy', 'N/A')}")
        print(f"   Sistema de sono: {status.get('sleep_system', {}).get('status', 'N/A')}")
        print(f"   Storage: {status.get('storage_status', 'N/A')}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🚀 TESTE REAL DO SISTEMA npllm")
    print("="*60)
    print("\nEste script testa o sistema completo com componentes reais.")
    print("Certifique-se de que:")
    print("  1. PostgreSQL está rodando (com pgvector)")
    print("  2. Modelos estão baixados")
    print("  3. Dependências estão instaladas")
    print("\n" + "="*60)
    
    input("\nPressione ENTER para continuar...")
    
    system = None
    
    try:
        # Teste 1: Query básica
        system, result = test_basic_query()
        
        if system:
            # Teste 2: Feedback
            test_feedback_capture(system, result)
            
            # Teste 3: Análise de projeto
            test_project_analysis(system)
            
            # Teste 4: Sono
            test_sleep_consolidation(system)
            
            # Teste 5: Status
            test_system_status(system)
        
        print("\n" + "="*60)
        print("✅ TESTES CONCLUÍDOS")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if system:
            print("\n🛑 Encerrando sistema...")
            try:
                system.close()
                print("✅ Sistema encerrado")
            except:
                pass


if __name__ == "__main__":
    main()

