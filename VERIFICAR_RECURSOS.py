#!/usr/bin/env python3
"""
Script para verificar recursos disponíveis na máquina
Compara com requisitos do sistema npllm
"""

import sys
import shutil
import psutil
import subprocess
from pathlib import Path


def format_bytes(bytes_value):
    """Formata bytes para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def check_disk_space():
    """Verifica espaço em disco"""
    print("\n" + "="*60)
    print("💾 ESPAÇO EM DISCO")
    print("="*60)
    
    disk = shutil.disk_usage('/')
    free_gb = disk.free / (1024**3)
    total_gb = disk.total / (1024**3)
    
    print(f"Total: {format_bytes(disk.total)}")
    print(f"Usado: {format_bytes(disk.used)}")
    print(f"Livre: {format_bytes(disk.free)}")
    
    # Requisitos: ~10GB (modelos + cache)
    required_gb = 10
    if free_gb >= required_gb:
        print(f"✅ Espaço suficiente ({free_gb:.1f}GB livre, necessário: {required_gb}GB)")
        return True
    else:
        print(f"⚠️  Espaço insuficiente ({free_gb:.1f}GB livre, necessário: {required_gb}GB)")
        return False


def check_ram():
    """Verifica RAM disponível"""
    print("\n" + "="*60)
    print("🧠 MEMÓRIA RAM")
    print("="*60)
    
    ram = psutil.virtual_memory()
    total_gb = ram.total / (1024**3)
    available_gb = ram.available / (1024**3)
    
    print(f"Total: {format_bytes(ram.total)}")
    print(f"Usado: {format_bytes(ram.used)}")
    print(f"Disponível: {format_bytes(ram.available)}")
    
    # Requisitos: 8GB mínimo, 16GB recomendado
    min_required_gb = 8
    recommended_gb = 16
    
    if available_gb >= recommended_gb:
        print(f"✅ RAM excelente ({available_gb:.1f}GB disponível, recomendado: {recommended_gb}GB)")
        return True
    elif available_gb >= min_required_gb:
        print(f"⚠️  RAM mínima ({available_gb:.1f}GB disponível, mínimo: {min_required_gb}GB, recomendado: {recommended_gb}GB)")
        return True
    else:
        print(f"❌ RAM insuficiente ({available_gb:.1f}GB disponível, mínimo: {min_required_gb}GB)")
        return False


def check_cpu():
    """Verifica CPU"""
    print("\n" + "="*60)
    print("⚙️  CPU")
    print("="*60)
    
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    
    print(f"Núcleos lógicos: {cpu_count}")
    if cpu_freq:
        print(f"Frequência: {cpu_freq.current:.0f} MHz")
    
    # Requisitos: 4+ cores recomendado
    min_cores = 2
    recommended_cores = 4
    
    if cpu_count >= recommended_cores:
        print(f"✅ CPU adequada ({cpu_count} cores, recomendado: {recommended_cores}+)")
        return True
    elif cpu_count >= min_cores:
        print(f"⚠️  CPU mínima ({cpu_count} cores, recomendado: {recommended_cores}+)")
        return True
    else:
        print(f"❌ CPU insuficiente ({cpu_count} cores, mínimo: {min_cores})")
        return False


def check_python():
    """Verifica Python e dependências"""
    print("\n" + "="*60)
    print("🐍 PYTHON")
    print("="*60)
    
    python_version = sys.version_info
    print(f"Versão: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor >= 8:
        print("✅ Python 3.8+ (requisito atendido)")
        return True
    else:
        print("❌ Python 3.8+ necessário")
        return False


def check_dependencies():
    """Verifica dependências Python"""
    print("\n" + "="*60)
    print("📦 DEPENDÊNCIAS PYTHON")
    print("="*60)
    
    required = {
        'torch': 'PyTorch',
        'transformers': 'Transformers',
        'peft': 'PEFT',
        'sentence_transformers': 'Sentence Transformers',
        'psycopg2': 'psycopg2 (PostgreSQL)',
        'numpy': 'NumPy',
        'loguru': 'Loguru'
    }
    
    missing = []
    for module, name in required.items():
        try:
            if module == 'psycopg2':
                import psycopg2
            else:
                __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (faltando)")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Instalar: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✅ Todas as dependências instaladas")
        return True


def check_postgresql():
    """Verifica PostgreSQL"""
    print("\n" + "="*60)
    print("🗄️  POSTGRESQL")
    print("="*60)
    
    # Verificar se psql está disponível
    psql_path = shutil.which('psql')
    if not psql_path:
        print("❌ PostgreSQL não encontrado (psql não está no PATH)")
        print("   Instalar: sudo apt-get install postgresql postgresql-contrib")
        return False
    
    print(f"✅ psql encontrado: {psql_path}")
    
    # Tentar verificar versão
    try:
        result = subprocess.run(
            ['psql', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   {result.stdout.strip()}")
    except:
        pass
    
    # Verificar se PostgreSQL está rodando
    try:
        result = subprocess.run(
            ['pg_isready'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ PostgreSQL está rodando")
            return True
        else:
            print("⚠️  PostgreSQL não está rodando")
            print("   Iniciar: sudo systemctl start postgresql")
            return False
    except FileNotFoundError:
        print("⚠️  pg_isready não encontrado")
        return False
    except:
        print("⚠️  Não foi possível verificar status do PostgreSQL")
        return False


def check_pgvector():
    """Verifica pgvector"""
    print("\n" + "="*60)
    print("🔍 PGVECTOR")
    print("="*60)
    
    try:
        import psycopg2
        # Tentar conectar e verificar extensão
        # Por enquanto, apenas informar
        print("⚠️  Verificação manual necessária")
        print("   Conectar ao PostgreSQL e executar:")
        print("   CREATE EXTENSION vector;")
        return None  # Não crítico para verificação inicial
    except ImportError:
        print("❌ psycopg2 não instalado")
        return False


def check_models():
    """Verifica espaço necessário para modelos"""
    print("\n" + "="*60)
    print("🤖 MODELOS")
    print("="*60)
    
    cache_dir = Path.home() / '.cache' / 'huggingface'
    if cache_dir.exists():
        import subprocess
        try:
            result = subprocess.run(
                ['du', '-sh', str(cache_dir)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                size = result.stdout.split()[0]
                print(f"Cache HuggingFace: {size}")
        except:
            pass
    
    print("\nModelos que serão baixados (primeira execução):")
    print("  - CodeLlama 3B: ~6GB")
    print("  - RoBERTa (sentiment): ~500MB")
    print("  - Total estimado: ~7GB")
    print("\n⚠️  Primeira execução pode demorar para baixar modelos")


def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🔍 VERIFICAÇÃO DE RECURSOS - Sistema npllm")
    print("="*60)
    
    results = {
        'disk': check_disk_space(),
        'ram': check_ram(),
        'cpu': check_cpu(),
        'python': check_python(),
        'dependencies': check_dependencies(),
        'postgresql': check_postgresql(),
        'pgvector': check_pgvector(),
    }
    
    check_models()
    
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    
    critical = ['disk', 'ram', 'python', 'dependencies']
    warnings = []
    errors = []
    
    for key, result in results.items():
        if result is None:
            continue
        if key in critical and not result:
            errors.append(key)
        elif not result:
            warnings.append(key)
    
    if errors:
        print(f"\n❌ PROBLEMAS CRÍTICOS: {', '.join(errors)}")
        print("   Corrija antes de executar o sistema")
        return False
    
    if warnings:
        print(f"\n⚠️  AVISOS: {', '.join(warnings)}")
        print("   Sistema pode funcionar, mas com limitações")
    
    print("\n✅ Sistema pode ser executado!")
    print("\nPróximos passos:")
    print("  1. Configurar PostgreSQL (se necessário)")
    print("  2. Instalar dependências faltantes (se houver)")
    print("  3. Executar: ./EXECUTAR_TESTE_REAL.sh")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificação interrompida")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro durante verificação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

