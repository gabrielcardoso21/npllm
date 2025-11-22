"""
End-to-End Integration Tests
Complete system flow from start to finish
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import Optional
from datetime import datetime, timedelta
from src.main import NpllmSystem
from src.feedback.implicit import UserAction


class TestEndToEnd:
    """End-to-end test suite"""
    
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
    @patch('src.main.ReplaySystem')
    @patch('src.main.FineTuningSystem')
    def test_complete_user_interaction_cycle(
        self,
        mock_fine_tuning,
        mock_replay,
        mock_adapter_manager,
        mock_emotional,
        mock_storage,
        mock_llm,
        mock_config
    ):
        """
        Test complete user interaction cycle:
        1. User sends query
        2. System processes and responds
        3. User provides feedback
        4. Feedback stored
        5. Sleep consolidation (after inactivity)
        """
        with patch('src.main.get_config', return_value=mock_config):
            # Setup all mocks
            mock_llm_instance = MagicMock()
            mock_llm_instance.generate.return_value = "def hello(): return 'world'"
            mock_llm_instance.get_hidden_size.return_value = 4096
            mock_llm.return_value = mock_llm_instance
            
            mock_storage_instance = MagicMock()
            mock_storage_instance.store_feedback.return_value = 1
            mock_storage_instance.get_all_feedbacks.return_value = [
                {
                    "id": 1,
                    "prompt": "Create hello function",
                    "response": "def hello(): return 'world'",
                    "score": 0.85,
                    "implicit_score": 0.8,
                    "emotional_score": 0.9,
                    "context": "python"
                }
            ]
            mock_storage_instance.get_important_examples.return_value = []
            mock_storage.return_value = mock_storage_instance
            
            mock_emotional_instance = MagicMock()
            mock_emotional_instance.analyze.return_value = {
                "sentiment": "positive",
                "signal": 0.9,
                "intensity": 0.9
            }
            mock_emotional.return_value = mock_emotional_instance
            
            mock_adapter_manager_instance = MagicMock()
            mock_adapter_manager_instance.get_adapter.return_value = None
            mock_adapter_manager.return_value = mock_adapter_manager_instance
            
            mock_replay_instance = MagicMock()
            mock_replay_instance.mix_examples.return_value = [
                {
                    "prompt": "Create hello function",
                    "response": "def hello(): return 'world'",
                    "score": 0.85,
                    "context": "python"
                }
            ]
            mock_replay.return_value = mock_replay_instance
            
            mock_fine_tuning_instance = MagicMock()
            mock_fine_tuning_instance.train_incremental.return_value = {
                "status": "success",
                "contexts_trained": 1
            }
            mock_fine_tuning_instance.update_adapters.return_value = {
                "status": "success",
                "adapters_updated": 1
            }
            mock_fine_tuning.return_value = mock_fine_tuning_instance
            
            # Initialize system
            system = NpllmSystem()
            
            # Step 1: Process query
            query = "Create a hello function in Python"
            result = system.process_query(
                query=query,
                file_path="test.py"
            )
            
            assert result is not None
            assert "response" in result
            assert result["adapter_used"] == "python_adapter"
            
            # Step 2: Capture feedback
            system.capture_feedback(
                query=query,
                response=result["response"],
                user_reaction="Perfect! Exactly what I needed.",
                user_action=UserAction.ACCEPT,
                explicit_feedback=0.9
            )
            
            # Verify feedback was stored
            mock_storage_instance.store_feedback.assert_called_once()
            call_args = mock_storage_instance.store_feedback.call_args
            assert call_args[1]["score"] > 0.7  # Positive feedback
            
            # Step 3: Simulate inactivity and trigger sleep
            system.sleep.last_activity = datetime.utcnow() - timedelta(minutes=31)
            sleep_result = system.trigger_sleep()
            
            assert sleep_result is not None
            assert sleep_result.get("status") == "success"
            
            # Verify fine-tuning was called
            mock_fine_tuning_instance.train_incremental.assert_called_once()
            mock_fine_tuning_instance.update_adapters.assert_called_once()
            
            # Step 4: Close system
            system.close()
            mock_storage_instance.close.assert_called_once()

