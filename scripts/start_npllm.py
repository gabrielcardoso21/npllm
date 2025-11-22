#!/usr/bin/env python3
"""
Script de inicialização do sistema npllm
Verifica dependências e inicia componentes
"""

import sys
import os
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("Verificando dependências...")
    
    required = [
        'torch',
        'transformers',
        'peft',
        'sentence_transformers',
        'psycopg2',
        'pgvector',
        'loguru',
        'pydantic',
    ]
    
    missing = []
    for dep in required:
        try:
            __import__(dep.replace('-', '_'))
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} (faltando)")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠ Dependências faltando: {', '.join(missing)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✓ Todas as dependências estão instaladas")
    return True


def check_docker_services():
    """Verifica se serviços Docker estão rodando"""
    print("\nVerificando serviços Docker...")
    
    import subprocess
    
    try:
        result = subprocess.run(
            ['docker', 'compose', 'ps', '--format', 'json'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("  ✓ Docker Compose disponível")
            
            # Verifica containers
            containers = ['npllm_postgres', 'npllm_redis']
            for container in containers:
                check = subprocess.run(
                    ['docker', 'ps', '--filter', f'name={container}', '--format', '{{.Names}}'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if container in check.stdout:
                    print(f"  ✓ {container} rodando")
                else:
                    print(f"  ⚠ {container} não encontrado")
            
            return True
        else:
            print("  ⚠ Docker Compose não disponível")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ⚠ Docker não encontrado ou não acessível")
        return False


def check_config():
    """Verifica configuração"""
    print("\nVerificando configuração...")
    
    try:
        from src.utils.config import get_config
        
        config = get_config()
        print(f"  ✓ Configuração carregada")
        print(f"    - Modelo: {config.model.base_model}")
        print(f"    - Database: {config.database.host}:{config.database.port}")
        return True
    except Exception as e:
        print(f"  ✗ Erro ao carregar configuração: {e}")
        return False


def initialize_system():
    """Inicializa sistema (sem carregar modelo completo)"""
    print("\nInicializando sistema...")
    
    try:
        from src.utils.logging import get_logger
        from src.utils.monitoring import ResourceMonitor
        
        logger = get_logger("startup")
        monitor = ResourceMonitor()
        
        # Verifica recursos
        mem = monitor.get_memory_usage()
        cpu = monitor.get_cpu_usage()
        
        print(f"  ✓ Logger inicializado")
        print(f"  ✓ Monitor de recursos ativo")
        print(f"    - Memória: {mem['process_memory_mb']:.1f} MB")
        print(f"    - CPU: {cpu['process_cpu_percent']:.1f}%")
        
        logger.info("npllm system initialized")
        return True
    except Exception as e:
        print(f"  ✗ Erro ao inicializar: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    print("=" * 60)
    print("INICIALIZAÇÃO DO SISTEMA npllm")
    print("=" * 60)
    
    checks = [
        ("Dependências", check_dependencies),
        ("Serviços Docker", check_docker_services),
        ("Configuração", check_config),
        ("Sistema", initialize_system),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Erro em {name}: {e}")
            results.append(False)
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, _) in enumerate(checks):
        status = "✓" if results[i] else "✗"
        print(f"{status} {name}")
    
    print(f"\nStatus: {passed}/{total} verificações passaram")
    
    if passed == total:
        print("\n✓ Sistema pronto para uso!")
        print("\nPróximos passos:")
        print("  1. Execute: python3 example_complete_workflow.py")
        print("  2. Ou use: python3 -m src.main")
        return 0
    else:
        print("\n⚠ Algumas verificações falharam")
        print("  Corrija os problemas antes de continuar")
        return 1


if __name__ == "__main__":
    sys.exit(main())

