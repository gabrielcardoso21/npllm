#!/usr/bin/env python3
"""
Teste direto do modelo para verificar se está gerando respostas
"""

import sys
from src.models.base_model import CodeLlamaBaseModel

def test_model():
    print("=" * 60)
    print("TESTE DIRETO DO MODELO")
    print("=" * 60)
    
    try:
        print("\n1. Carregando modelo...")
        model = CodeLlamaBaseModel()
        print("✅ Modelo carregado")
        
        print("\n2. Testando geração simples...")
        prompt = "Olá! Como você está?"
        print(f"   Prompt: {prompt}")
        
        response = model.generate(prompt, max_length=100, stream=False)
        
        print(f"\n3. Resposta recebida:")
        print(f"   Type: {type(response)}")
        print(f"   Is string: {isinstance(response, str)}")
        print(f"   Length: {len(response) if isinstance(response, str) else 'N/A'}")
        print(f"   Value: {repr(response[:200])}")
        
        if not response or response.strip() == "":
            print("\n❌ PROBLEMA: Resposta está vazia!")
            return False
        else:
            print(f"\n✅ SUCESSO: Resposta gerada ({len(response)} caracteres)")
            print(f"\nResposta completa:\n{response}")
            return True
            
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model()
    sys.exit(0 if success else 1)

