"""
Tests for Architectural Analysis
TDD: Tests first
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from src.analysis.architecture import ArchitectureAnalyzer


class TestArchitectureAnalyzer:
    """Test suite for ArchitectureAnalyzer"""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = ArchitectureAnalyzer()
        assert analyzer is not None
    
    def test_parse_directory_structure(self, temp_dir):
        """Test parsing directory structure"""
        # Create test directory structure
        (temp_dir / "src").mkdir()
        (temp_dir / "tests").mkdir()
        (temp_dir / "src" / "models").mkdir()
        (temp_dir / "src" / "adapters").mkdir()
        
        analyzer = ArchitectureAnalyzer()
        structure = analyzer.parse_directory_structure(str(temp_dir))
        
        assert "src" in structure
        assert "tests" in structure
        assert "models" in structure["src"]
    
    def test_identify_design_patterns(self):
        """Test identification of design patterns"""
        analyzer = ArchitectureAnalyzer()
        
        # Mock code that uses Repository pattern
        code = """
        class UserRepository:
            def __init__(self, db):
                self.db = db
            
            def find_by_id(self, id):
                return self.db.query(User).filter_by(id=id).first()
        """
        
        patterns = analyzer.identify_design_patterns(code)
        assert isinstance(patterns, list)
    
    def test_extract_architectural_decisions(self):
        """Test extraction of architectural decisions"""
        analyzer = ArchitectureAnalyzer()
        
        structure = {
            "src": {
                "models": {},
                "adapters": {},
                "storage": {}
            }
        }
        
        decisions = analyzer.extract_architectural_decisions(structure)
        assert isinstance(decisions, list)

