"""
Tests for Pattern Identification
TDD: Tests first
"""

import pytest
from src.analysis.patterns import PatternIdentifier


class TestPatternIdentifier:
    """Test suite for PatternIdentifier"""
    
    def test_identifier_initialization(self):
        """Test identifier initialization"""
        identifier = PatternIdentifier()
        assert identifier is not None
        assert hasattr(identifier, 'patterns_db')
    
    def test_identify_common_patterns(self):
        """Test identifying common patterns"""
        identifier = PatternIdentifier()
        
        project_analyses = [
            {
                "project_path": "/project1",
                "patterns_found": ["repository", "factory"]
            },
            {
                "project_path": "/project2",
                "patterns_found": ["repository", "mvc"]
            },
            {
                "project_path": "/project3",
                "patterns_found": ["factory"]
            }
        ]
        
        common_patterns = identifier.identify_common_patterns(project_analyses)
        
        # Repository appears in 2 projects, factory in 2 projects
        assert len(common_patterns) >= 2
        assert any(p["pattern"] == "repository" for p in common_patterns)
        assert any(p["pattern"] == "factory" for p in common_patterns)
    
    def test_extract_general_concepts(self):
        """Test extracting general concepts"""
        identifier = PatternIdentifier()
        
        patterns = [
            {
                "pattern": "repository",
                "frequency": 2,
                "projects": ["/p1", "/p2"],
                "generalization": {
                    "concept": "Data access abstraction",
                    "applicable_to": ["Python", "Java"],
                    "use_cases": ["Database access"]
                }
            }
        ]
        
        concepts = identifier.extract_general_concepts(patterns)
        
        assert len(concepts) == 1
        assert concepts[0]["concept"] == "Data access abstraction"
    
    def test_consolidate_knowledge(self):
        """Test knowledge consolidation"""
        identifier = PatternIdentifier()
        
        patterns = [
            {
                "pattern": "repository",
                "frequency": 2,
                "projects": ["/p1", "/p2"],
                "generalization": {
                    "concept": "Data access abstraction",
                    "applicable_to": ["Python"],
                    "use_cases": ["Database"]
                }
            }
        ]
        
        consolidated = identifier.consolidate_knowledge(patterns)
        
        assert "patterns" in consolidated
        assert "concepts" in consolidated
        assert consolidated["total_patterns"] == 1

