"""
Integration Tests: Architecture Analysis Flow
Tests the complete architecture analysis and pattern learning flow
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import Optional
from pathlib import Path
import tempfile
from src.main import NpllmSystem


class TestArchitectureFlow:
    """Test suite for architecture analysis flow"""
    
    @pytest.fixture
    def temp_project(self, tmp_path):
        """Create temporary project structure"""
        project = tmp_path / "test_project"
        project.mkdir()
        
        # Create directory structure
        (project / "src").mkdir()
        (project / "tests").mkdir()
        (project / "src" / "models").mkdir()
        (project / "src" / "adapters").mkdir()
        
        # Create sample files
        (project / "src" / "models" / "user.py").write_text("""
class UserRepository:
    def __init__(self, db):
        self.db = db
    
    def find_by_id(self, id):
        return self.db.query(User).filter_by(id=id).first()
""")
        
        (project / "main.py").write_text("""
from src.models.user import UserRepository

def main():
    repo = UserRepository(db)
    user = repo.find_by_id(1)
""")
        
        return str(project)
    
    @patch('src.main.CodeLlamaBaseModel')
    @patch('src.main.PostgreSQLStorage')
    @patch('src.main.EmotionalAnalyzer')
    @patch('src.main.AdapterManager')
    def test_project_analysis(self, mock_adapter_manager, mock_emotional, mock_storage, mock_llm, mock_config, temp_project):
        """Test project architecture analysis"""
        with patch('src.main.get_config', return_value=mock_config):
            # Setup mocks
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
            
            # Analyze project
            analysis = system.analyze_project(temp_project)
            
            assert analysis is not None
            assert "structure" in analysis
            assert "patterns_found" in analysis
            assert "repository" in analysis.get("patterns_found", [])
    
    @patch('src.main.CodeLlamaBaseModel')
    @patch('src.main.PostgreSQLStorage')
    @patch('src.main.EmotionalAnalyzer')
    @patch('src.main.AdapterManager')
    def test_architecture_suggestion(self, mock_adapter_manager, mock_emotional, mock_storage, mock_llm, mock_config):
        """Test architecture suggestion for new project"""
        with patch('src.main.get_config', return_value=mock_config):
            # Setup mocks
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
            
            # Suggest architecture
            suggestion = system.suggest_architecture("/new_project")
            
            assert suggestion is not None
            assert "recommended_patterns" in suggestion
            assert "suggested_structure" in suggestion

