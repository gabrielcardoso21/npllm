#!/usr/bin/env python3
"""
Script de teste local com modelo menor (TinyLlama)
"""

import sys
from src.models.base_model import CodeLlamaBaseModel
from src.main import initialize_system

def test_model_direct():
    """Testa o modelo diretamente"""
    print("=" * 60)
    print("TESTE 1: Modelo Base Diretamente")
    print("=" * 60)
    
    try:
        print("Carregando modelo TinyLlama...")
        m = CodeLlamaBaseModel()
        print("✅ Modelo carregado!")
        
        print("\nGerando resposta...")
        r = m.generate("Olá! Como você está?", max_length=50, stream=False)
        
        print(f"\n✅ Type: {type(r)}")
        print(f"✅ Is string: {isinstance(r, str)}")
        print(f"✅ Response: {r[:200]}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_system():
    """Testa o sistema completo"""
    print("\n" + "=" * 60)
    print("TESTE 2: Sistema Completo")
    print("=" * 60)
    
    try:
        print("Inicializando sistema...")
        s = initialize_system()
        print("✅ Sistema inicializado!")
        
        print("\nProcessando query...")
        r = s.process_query("Olá!")
        
        print(f"\n✅ Type: {type(r['response'])}")
        print(f"✅ Is string: {isinstance(r['response'], str)}")
        print(f"✅ Response: {r['response'][:200]}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🧪 TESTE LOCAL COM MODELO MENOR (TinyLlama)\n")
    
    result1 = test_model_direct()
    print("\n")
    result2 = test_system()
    
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    print(f"Teste 1 (Modelo Direto): {'✅ PASSOU' if result1 else '❌ FALHOU'}")
    print(f"Teste 2 (Sistema Completo): {'✅ PASSOU' if result2 else '❌ FALHOU'}")
    
    if result1 and result2:
        print("\n🎉 Todos os testes passaram!")
        sys.exit(0)
    else:
        print("\n⚠️ Alguns testes falharam")
        sys.exit(1)

