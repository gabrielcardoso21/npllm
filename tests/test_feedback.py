"""
Tests for Feedback Systems
TDD: Tests first
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.feedback.emotional import EmotionalAnalyzer
from src.feedback.implicit import ImplicitFeedback, UserAction


class TestEmotionalAnalyzer:
    """Test suite for EmotionalAnalyzer"""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = EmotionalAnalyzer()
        assert analyzer is not None
        assert analyzer.model_name is not None
        assert analyzer._model is None  # Lazy loading
    
    def test_analyze_empty_text(self):
        """Test analysis of empty text"""
        analyzer = EmotionalAnalyzer()
        result = analyzer.analyze("")
        assert result["sentiment"] == "neutral"
        assert result["signal"] == 0.0
    
    @patch('src.feedback.emotional.AutoTokenizer')
    @patch('src.feedback.emotional.AutoModelForSequenceClassification')
    def test_analyze_text(self, mock_model_class, mock_tokenizer_class):
        """Test analysis of text"""
        import torch
        
        # Mock tokenizer - precisa simular tokenizer(text).to(device)
        mock_tokenizer_instance = MagicMock()
        # Quando tokenizer(text, ...) é chamado, retorna dict
        tokenized_dict = {"input_ids": torch.tensor([[1, 2, 3]])}
        mock_tokenizer_instance.return_value = tokenized_dict
        # Quando .to(device) é chamado no dict, retorna o mesmo dict
        tokenized_dict['to'] = MagicMock(return_value=tokenized_dict)
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer_instance
        
        # Mock model
        mock_model_instance = MagicMock()
        mock_outputs = MagicMock()
        mock_outputs.logits = torch.tensor([[[0.1, 0.2, 0.7]]])  # positive > negative > neutral
        # Quando model(**inputs) é chamado
        mock_model_instance.__call__ = MagicMock(return_value=mock_outputs)
        mock_model_instance.to = MagicMock(return_value=mock_model_instance)
        mock_model_instance.eval = MagicMock()
        mock_model_class.from_pretrained.return_value = mock_model_instance
        
        analyzer = EmotionalAnalyzer()
        result = analyzer.analyze("This is great!")
        
        # Should detect positive sentiment
        assert "sentiment" in result
        assert "signal" in result
    
    def test_get_emotional_reward(self):
        """Test getting emotional reward"""
        analyzer = EmotionalAnalyzer()
        # Will be tested with actual model loading


class TestImplicitFeedback:
    """Test suite for ImplicitFeedback"""
    
    def test_feedback_initialization(self):
        """Test feedback initialization"""
        feedback = ImplicitFeedback()
        assert feedback is not None
        assert hasattr(feedback, 'interaction_history')
        assert isinstance(feedback.interaction_history, list)
    
    def test_track_interaction_accept(self):
        """Test tracking accept action"""
        feedback = ImplicitFeedback()
        feedback.track_interaction(
            suggestion_id="test_1",
            user_action=UserAction.ACCEPT
        )
        
        assert len(feedback.interaction_history) == 1
        assert feedback.interaction_history[0]["action"] == "accept"
    
    def test_calculate_reward_accept_no_edit(self):
        """Test reward calculation for accept without edit"""
        feedback = ImplicitFeedback()
        reward = feedback.calculate_reward(UserAction.ACCEPT, edit_distance=0.05)
        assert reward == 1.0
    
    def test_calculate_reward_accept_small_edit(self):
        """Test reward calculation for accept with small edit"""
        feedback = ImplicitFeedback()
        reward = feedback.calculate_reward(UserAction.ACCEPT, edit_distance=0.2)
        assert reward == 0.8
    
    def test_calculate_reward_delete(self):
        """Test reward calculation for delete"""
        feedback = ImplicitFeedback()
        reward = feedback.calculate_reward(UserAction.DELETE)
        assert reward == -0.5
    
    def test_calculate_reward_ignore(self):
        """Test reward calculation for ignore"""
        feedback = ImplicitFeedback()
        reward = feedback.calculate_reward(UserAction.IGNORE)
        assert reward == -0.1

