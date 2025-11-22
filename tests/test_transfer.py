"""
Tests for Transfer Learning
TDD: Tests first
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.transfer.learning import TransferLearning


class TestTransferLearning:
    """Test suite for TransferLearning"""
    
    def test_transfer_initialization(self):
        """Test transfer learning initialization"""
        mock_storage = Mock()
        transfer = TransferLearning(mock_storage)
        assert transfer is not None
        assert transfer.storage == mock_storage
    
    def test_apply_patterns(self):
        """Test applying patterns to target project"""
        mock_storage = Mock()
        transfer = TransferLearning(mock_storage)
        
        source_patterns = [
            {
                "pattern": "repository",
                "frequency": 2,
                "projects": ["/p1", "/p2"],
                "generalization": {
                    "concept": "Data access",
                    "applicable_to": ["Python"]
                }
            }
        ]
        
        target_structure = {
            "project_path": "/target",
            "src": {}
        }
        
        applied = transfer.apply_patterns(source_patterns, target_structure)
        
        assert len(applied) > 0
        assert applied[0]["pattern"] == "repository"
    
    def test_suggest_architecture(self):
        """Test architecture suggestion"""
        mock_storage = Mock()
        transfer = TransferLearning(mock_storage)
        
        learned_patterns = [
            {
                "pattern": "mvc",
                "frequency": 3,
                "score": 0.9,
                "projects": ["/p1", "/p2", "/p3"]
            },
            {
                "pattern": "repository",
                "frequency": 2,
                "score": 0.8,
                "projects": ["/p1", "/p2"]
            }
        ]
        
        suggestion = transfer.suggest_architecture("/target", learned_patterns)
        
        assert "recommended_patterns" in suggestion
        assert "suggested_structure" in suggestion
        assert "mvc" in suggestion["recommended_patterns"]

