"""
Tests for LoRA Adapters
TDD: Tests first
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.adapters.lora_adapter import LoRAAdapter
from src.adapters.manager import AdapterManager
from src.adapters.selector import AdapterSelector


class TestLoRAAdapter:
    """Test suite for LoRAAdapter"""
    
    def test_adapter_initialization(self):
        """Test adapter initialization"""
        mock_base_model = MagicMock()
        
        with patch('src.adapters.lora_adapter.get_peft_model') as mock_peft:
            mock_peft_model = MagicMock()
            mock_peft.return_value = mock_peft_model
            
            adapter = LoRAAdapter(
                base_model=mock_base_model,
                name="test_adapter",
                context="python",
                version="stable"
            )
            
            assert adapter is not None
            assert adapter.name == "test_adapter"
            assert adapter.context == "python"
            assert adapter.version == "stable"
    
    def test_adapter_invalid_version(self):
        """Test adapter with invalid version"""
        mock_base_model = MagicMock()
        
        with pytest.raises(ValueError):
            LoRAAdapter(
                base_model=mock_base_model,
                name="test",
                context="python",
                version="invalid"
            )
    
    def test_adapter_getters(self):
        """Test adapter getter methods"""
        mock_base_model = MagicMock()
        
        with patch('src.adapters.lora_adapter.get_peft_model'):
            adapter = LoRAAdapter(
                base_model=mock_base_model,
                name="test_adapter",
                context="python",
                version="stable"
            )
            
            assert adapter.get_name() == "test_adapter"
            assert adapter.get_context() == "python"
            assert adapter.get_version() == "stable"


class TestAdapterManager:
    """Test suite for AdapterManager"""
    
    def test_manager_initialization(self, mock_config):
        """Test manager initialization"""
        mock_base_model = MagicMock()
        
        with patch('src.adapters.manager.get_config', return_value=mock_config):
            manager = AdapterManager(mock_base_model)
            assert manager is not None
            assert manager.base_model == mock_base_model
    
    def test_create_adapter(self, mock_config):
        """Test creating adapter"""
        mock_base_model = MagicMock()
        mock_base_model._model = MagicMock()
        
        with patch('src.adapters.manager.get_config', return_value=mock_config):
            with patch('src.adapters.lora_adapter.get_peft_model'):
                manager = AdapterManager(mock_base_model)
                adapter = manager.create_adapter(
                    name="test",
                    context="python",
                    version="stable"
                )
                
                assert adapter is not None
                assert adapter.get_context() == "python"

