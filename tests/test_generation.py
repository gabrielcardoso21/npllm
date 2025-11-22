"""
Tests for Architectural Generation
TDD: Tests first
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.generation.architectural import ArchitecturalGenerator


class TestArchitecturalGenerator:
    """Test suite for ArchitecturalGenerator"""
    
    def test_generator_initialization(self):
        """Test generator initialization"""
        mock_llm = Mock()
        generator = ArchitecturalGenerator(mock_llm)
        assert generator is not None
        assert generator.llm == mock_llm
    
    def test_generate_project_structure(self):
        """Test generating project structure"""
        mock_llm = Mock()
        mock_llm.generate.return_value = """
        src/
        ├── models/
        ├── adapters/
        └── storage/
        """
        
        generator = ArchitecturalGenerator(mock_llm)
        structure = generator.generate_project_structure(
            patterns=["repository", "mvc"],
            project_name="test_project"
        )
        
        assert structure is not None
        mock_llm.generate.assert_called()
    
    def test_generate_module(self):
        """Test generating module"""
        mock_llm = Mock()
        mock_llm.generate.return_value = "class UserRepository:\n    pass"
        
        generator = ArchitecturalGenerator(mock_llm)
        module = generator.generate_module(
            module_type="repository",
            context="user"
        )
        
        assert module is not None
        assert "class" in module or "def" in module
    
    def test_generate_configuration(self):
        """Test generating configuration"""
        mock_llm = Mock()
        mock_llm.generate.return_value = "database:\n  host: localhost"
        
        generator = ArchitecturalGenerator(mock_llm)
        config = generator.generate_configuration(
            config_type="database",
            project_type="web"
        )
        
        assert config is not None

