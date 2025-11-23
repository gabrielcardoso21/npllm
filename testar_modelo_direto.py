#!/usr/bin/env python3
"""
Script simples para testar o modelo diretamente (sem API)
Uso: python3 testar_modelo_direto.py "sua pergunta aqui"
"""

import sys
import os
import time
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.models.base_model import CodeLlamaBaseModel
from src.models.api_model import APIModel
from src.utils.config import get_config
from src.utils.logging import get_logger

logger = get_logger("test_modelo_direto")


def main():
    """Testa o modelo diretamente"""
    # Pega a pergunta dos argumentos ou usa padrão
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Olá! Como você está?"
    
    print(f"🤖 Testando modelo diretamente...")
    print(f"📝 Pergunta: {query}")
    print(f"{'='*60}\n")
    
    try:
        # Inicializa modelo (local ou API)
        print("⏳ Carregando modelo...")
        start_init = time.time()
        
        config = get_config()
        model_config = config.model
        model_mode = model_config.mode or os.getenv('MODEL_MODE', 'local')
        
        if model_mode == "api":
            provider = model_config.provider or os.getenv('MODEL_PROVIDER', 'groq')
            print(f"🌐 Usando API: {provider}")
            model = APIModel(provider=provider)
        else:
            print("💻 Usando modelo local")
            model = CodeLlamaBaseModel()
        
        init_time = time.time() - start_init
        print(f"✅ Modelo inicializado em {init_time:.2f}s\n")
        
        # Gera resposta com streaming
        print("⏳ Gerando resposta (streaming)...\n")
        print(f"{'='*60}")
        print("🤖 Resposta (streaming):\n")
        
        start_gen = time.time()
        response_parts = []
        
        # Itera sobre os tokens conforme são gerados
        # Sem limite de tokens - gera resposta completa
        try:
            for token in model.generate(
                query,
                max_length=8192,  # Sem limite - resposta completa
                temperature=0.7,
                stream=True
            ):
                # Imprime token imediatamente (sem quebra de linha)
                print(token, end='', flush=True)
                response_parts.append(token)
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrompido pelo usuário")
        except Exception as e:
            print(f"\n\n❌ Erro durante streaming: {e}")
            import traceback
            traceback.print_exc()
        
        gen_time = time.time() - start_gen
        full_response = ''.join(response_parts)
        
        # Mostra resultado
        print(f"\n\n{'='*60}")
        print(f"✅ Resposta gerada em {gen_time:.2f}s")
        print(f"{'='*60}")
        print(f"📊 Estatísticas:")
        print(f"   • Tempo de inicialização: {init_time:.2f}s")
        print(f"   • Tempo de geração: {gen_time:.2f}s")
        print(f"   • Tempo total: {init_time + gen_time:.2f}s")
        print(f"   • Tamanho da resposta: {len(full_response)} caracteres")
        print(f"   • Tokens gerados: {len(response_parts)}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

