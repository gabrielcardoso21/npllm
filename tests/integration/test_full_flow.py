"""
Integration Tests: Full Flow
Tests the complete system flow from query to feedback to sleep
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import Optional
from src.main import NpllmSystem
from src.feedback.implicit import UserAction


class TestFullFlow:
    """Test suite for full system flow"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration"""
        config = MagicMock()
        config.model.base_model = "codellama/CodeLlama-3b-Instruct-hf"
        config.model.device = "cpu"
        config.model.max_memory = None
        config.database.host = "localhost"
        config.database.port = 5432
        config.database.database = "npllm_test"
        config.database.user = "test_user"
        config.database.password = "test_password"
        config.database.pool_size = 5
        config.get_section.return_value = {
            "lora": {
                "r": 16,
                "lora_alpha": 32,
                "lora_dropout": 0.1,
                "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"]
            }
        }
        return config
    
    @patch('src.main.CodeLlamaBaseModel')
    @patch('src.main.PostgreSQLStorage')
    @patch('src.main.EmotionalAnalyzer')
    @patch('src.main.AdapterManager')
    def test_system_initialization(self, mock_adapter_manager, mock_emotional, mock_storage, mock_llm, mock_config):
        """Test complete system initialization"""
        with patch('src.main.get_config', return_value=mock_config):
            # Mock all components
            mock_llm_instance = MagicMock()
            mock_llm_instance.get_hidden_size.return_value = 4096
            mock_llm.return_value = mock_llm_instance
            
            mock_storage_instance = MagicMock()
            mock_storage.return_value = mock_storage_instance
            
            mock_emotional_instance = MagicMock()
            mock_emotional.return_value = mock_emotional_instance
            
            mock_adapter_manager_instance = MagicMock()
            mock_adapter_manager.return_value = mock_adapter_manager_instance
            
            system = NpllmSystem()
            
            assert system is not None
            assert system.base_model is not None
            assert system.selector is not None
            assert system.storage is not None
            assert system.emotional_analyzer is not None
            assert system.sleep is not None
    
    @patch('src.main.CodeLlamaBaseModel')
    @patch('src.main.PostgreSQLStorage')
    @patch('src.main.EmotionalAnalyzer')
    @patch('src.main.AdapterManager')
    def test_query_processing_flow(self, mock_adapter_manager, mock_emotional, mock_storage, mock_llm, mock_config):
        """Test complete query processing flow"""
        with patch('src.main.get_config', return_value=mock_config):
            # Setup mocks
            mock_llm_instance = MagicMock()
            mock_llm_instance.generate.return_value = "def hello(): return 'world'"
            mock_llm_instance.get_hidden_size.return_value = 4096
            mock_llm.return_value = mock_llm_instance
            
            mock_storage_instance = MagicMock()
            mock_storage.return_value = mock_storage_instance
            
            mock_emotional_instance = MagicMock()
            mock_emotional_instance.analyze.return_value = {
                "sentiment": "positive",
                "signal": 0.8
            }
            mock_emotional.return_value = mock_emotional_instance
            
            mock_adapter_manager_instance = MagicMock()
            mock_adapter_manager_instance.get_adapter.return_value = None
            mock_adapter_manager.return_value = mock_adapter_manager_instance
            
            system = NpllmSystem()
            
            # Process query
            result = system.process_query(
                query="Create a hello function",
                file_path="test.py"
            )
            
            assert result is not None
            assert "response" in result
            assert "adapter_used" in result
            assert result["adapter_used"] == "python_adapter"  # Selected by extension
    
    @patch('src.main.CodeLlamaBaseModel')
    @patch('src.main.PostgreSQLStorage')
    @patch('src.main.EmotionalAnalyzer')
    @patch('src.main.AdapterManager')
    def test_feedback_capture_flow(self, mock_adapter_manager, mock_emotional, mock_storage, mock_llm, mock_config):
        """Test feedback capture and storage flow"""
        with patch('src.main.get_config', return_value=mock_config):
            # Setup mocks
            mock_llm_instance = MagicMock()
            mock_llm_instance.get_hidden_size.return_value = 4096
            mock_llm.return_value = mock_llm_instance
            
            mock_storage_instance = MagicMock()
            mock_storage_instance.store_feedback.return_value = 1
            mock_storage.return_value = mock_storage_instance
            
            mock_emotional_instance = MagicMock()
            mock_emotional_instance.analyze.return_value = {
                "sentiment": "positive",
                "signal": 0.9
            }
            mock_emotional.return_value = mock_emotional_instance
            
            mock_adapter_manager_instance = MagicMock()
            mock_adapter_manager.return_value = mock_adapter_manager_instance
            
            system = NpllmSystem()
            system._last_adapter_name = "python_adapter"
            
            # Capture feedback
            system.capture_feedback(
                query="Create a hello function",
                response="def hello(): return 'world'",
                user_reaction="Great! This is exactly what I needed.",
                user_action=UserAction.ACCEPT,
                explicit_feedback=0.9
            )
            
            # Verify storage was called
            mock_storage_instance.store_feedback.assert_called_once()
            call_args = mock_storage_instance.store_feedback.call_args
            assert call_args[1]["score"] > 0.7  # Positive feedback
    
    @patch('src.main.CodeLlamaBaseModel')
    @patch('src.main.PostgreSQLStorage')
    @patch('src.main.EmotionalAnalyzer')
    @patch('src.main.AdapterManager')
    @patch('src.main.ReplaySystem')
    @patch('src.main.FineTuningSystem')
    def test_sleep_consolidation_flow(
        self,
        mock_fine_tuning,
        mock_replay,
        mock_adapter_manager,
        mock_emotional,
        mock_storage,
        mock_llm,
        mock_config
    ):
        """Test sleep consolidation flow"""
        with patch('src.main.get_config', return_value=mock_config):
            # Setup mocks
            mock_llm_instance = MagicMock()
            mock_llm_instance.get_hidden_size.return_value = 4096
            mock_llm.return_value = mock_llm_instance
            
            mock_storage_instance = MagicMock()
            mock_storage_instance.get_all_feedbacks.return_value = [
                {"id": 1, "prompt": "test", "response": "result", "score": 0.9, "context": "python"}
            ]
            mock_storage_instance.get_important_examples.return_value = []
            mock_storage.return_value = mock_storage_instance
            
            mock_emotional_instance = MagicMock()
            mock_emotional.return_value = mock_emotional_instance
            
            mock_adapter_manager_instance = MagicMock()
            mock_adapter_manager.return_value = mock_adapter_manager_instance
            
            mock_replay_instance = MagicMock()
            mock_replay_instance.mix_examples.return_value = [
                {"prompt": "test", "response": "result", "score": 0.9}
            ]
            mock_replay.return_value = mock_replay_instance
            
            mock_fine_tuning_instance = MagicMock()
            mock_fine_tuning_instance.train_incremental.return_value = {"status": "success"}
            mock_fine_tuning_instance.update_adapters.return_value = {"status": "success"}
            mock_fine_tuning.return_value = mock_fine_tuning_instance
            
            system = NpllmSystem()
            
            # Simulate inactivity
            from datetime import datetime, timedelta
            system.sleep.last_activity = datetime.utcnow() - timedelta(minutes=31)
            
            # Trigger sleep
            result = system.trigger_sleep()
            
            assert result is not None
            assert result.get("status") == "success"
            mock_fine_tuning_instance.train_incremental.assert_called_once()
            mock_fine_tuning_instance.update_adapters.assert_called_once()

