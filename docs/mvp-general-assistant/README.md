# MVP: Assistente Geral de Código com Aprendizado Arquitetural

Este diretório contém a documentação consolidada do MVP do assistente geral de código com foco em arquitetura e transfer learning entre projetos.

## Documentos

- **[ARQUITETURA-FINAL.md](./ARQUITETURA-FINAL.md)** - Arquitetura final simplificada do sistema com diagramas e fluxos detalhados
- **[IMPLEMENTACAO-MVP.md](./IMPLEMENTACAO-MVP.md)** - Plano de implementação completo com fases, tarefas e checklist

## Objetivo do MVP

Criar um assistente de código geral que:
- Aprende padrões arquiteturais de qualquer projeto
- Aprende em um projeto e aplica em outro (transfer learning)
- Foca em arquitetura e engenharia, não código de baixo nível
- Aprende continuamente e melhora com o tempo
- Processa feedback emocional para guiar aprendizado
- Prepara programadores para o futuro: arquitetar e gerenciar IA

## Filosofia

**O futuro é de quem sabe arquitetar e gerenciar IA, não de quem escreve código de baixo/médio nível.**

## Arquitetura Simplificada

O sistema foi simplificado significativamente, mantendo apenas 6 componentes essenciais:
1. LLM Base (CodeLlama 3B) - Não treina
2. Seletor de Adapter - Seleção direta por contexto
3. LoRA Adapters - Treina apenas durante sono
4. PostgreSQL + pgvector - Armazenamento
5. Análise Emocional (RoBERTa) - Captura emoção
6. Sistema de Sono - Consolidação durante inatividade

## Status

✅ **Arquitetura Definida** - Pronto para implementação

## Próximos Passos

1. ✅ Arquitetura final definida
2. ✅ Plano de implementação criado
3. ⏳ Iniciar Fase 1: Setup e Base

