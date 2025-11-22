-- Script de inicialização do banco de dados
-- Executado automaticamente quando o container PostgreSQL é criado

-- Criar extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Criar schema para npllm
CREATE SCHEMA IF NOT EXISTS npllm;

-- Criar tabela de embeddings (será criada pelo código Python)
-- Mas podemos criar a estrutura básica aqui se necessário

-- Criar índices otimizados (será feito pelo código Python)
-- Mas podemos preparar aqui

-- Log
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully';
END $$;

