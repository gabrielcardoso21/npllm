"""
Tests for PostgreSQL Storage
TDD: Tests first
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import numpy as np
from src.storage.postgres import PostgreSQLStorage


class TestPostgreSQLStorage:
    """Test suite for PostgreSQLStorage"""
    
    def test_storage_initialization(self, mock_config):
        """Test storage initialization"""
        with patch('src.storage.postgres.get_config', return_value=mock_config):
            with patch('src.storage.postgres.ThreadedConnectionPool') as mock_pool:
                with patch('src.storage.postgres.register_vector') as mock_register:
                    mock_conn = MagicMock()
                    mock_pool.return_value.getconn.return_value = mock_conn
                    mock_pool.return_value.putconn = Mock()
                    
                    storage = PostgreSQLStorage()
                    assert storage is not None
                    assert hasattr(storage, 'pool')
                    mock_register.assert_called_once()
    
    def test_store_feedback(self, mock_config):
        """Test storing feedback"""
        with patch('src.storage.postgres.get_config', return_value=mock_config):
            with patch('src.storage.postgres.ThreadedConnectionPool') as mock_pool:
                with patch('src.storage.postgres.register_vector'):
                    mock_conn = MagicMock()
                    mock_cursor = MagicMock()
                    mock_cursor.fetchone.return_value = [1]
                    mock_conn.cursor.return_value = mock_cursor
                    mock_pool.return_value.getconn.return_value = mock_conn
                    mock_pool.return_value.putconn = Mock()
                    
                    storage = PostgreSQLStorage()
                    feedback_id = storage.store_feedback(
                        prompt="test prompt",
                        response="test response",
                        score=0.8,
                        implicit_score=0.7,
                        emotional_score=0.9,
                        context="python"
                    )
                    
                    assert feedback_id == 1
                    mock_cursor.execute.assert_called()
    
    def test_get_all_feedbacks(self, mock_config):
        """Test getting all feedbacks"""
        with patch('src.storage.postgres.get_config', return_value=mock_config):
            with patch('src.storage.postgres.ThreadedConnectionPool') as mock_pool:
                with patch('src.storage.postgres.register_vector'):
                    mock_conn = MagicMock()
                    mock_cursor = MagicMock()
                    # Tuple com 8 elementos: id, prompt, response, score, implicit_score, emotional_score, context, created_at
                    mock_cursor.fetchall.return_value = [
                        (1, "prompt1", "response1", 0.8, 0.7, 0.9, "python", "2025-01-27")
                    ]
                    mock_conn.cursor.return_value = mock_cursor
                    mock_pool.return_value.getconn.return_value = mock_conn
                    mock_pool.return_value.putconn = Mock()
                    
                    storage = PostgreSQLStorage()
                    feedbacks = storage.get_all_feedbacks()
                    
                    assert len(feedbacks) == 1
                    assert feedbacks[0]["score"] == 0.8
    
    def test_get_important_examples(self, mock_config):
        """Test getting important examples"""
        with patch('src.storage.postgres.get_config', return_value=mock_config):
            with patch('src.storage.postgres.ThreadedConnectionPool') as mock_pool:
                with patch('src.storage.postgres.register_vector'):
                    mock_conn = MagicMock()
                    mock_cursor = MagicMock()
                    # Tuple com 6 elementos: id, prompt, response, score, context, created_at
                    mock_cursor.fetchall.return_value = [
                        (1, "prompt1", "response1", 0.9, "python", "2025-01-27")
                    ]
                    mock_conn.cursor.return_value = mock_cursor
                    mock_pool.return_value.getconn.return_value = mock_conn
                    mock_pool.return_value.putconn = Mock()
                    
                    storage = PostgreSQLStorage()
                    examples = storage.get_important_examples(limit=10)
                    
                    assert len(examples) == 1
                    assert examples[0]["score"] == 0.9

