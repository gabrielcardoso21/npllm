"""
Tests for Adapter Selector
TDD: Tests first, implementation already done
"""

import pytest
from src.adapters.selector import AdapterSelector


class TestAdapterSelector:
    """Test suite for AdapterSelector"""
    
    def test_selector_initialization(self):
        """Test selector initialization"""
        selector = AdapterSelector()
        assert selector is not None
        assert hasattr(selector, 'extension_map')
        assert hasattr(selector, 'project_structure_map')
    
    def test_select_by_extension_python(self):
        """Test selection by Python file extension"""
        selector = AdapterSelector()
        adapter = selector.select(file_path="test.py")
        assert adapter == "python_adapter"
    
    def test_select_by_extension_javascript(self):
        """Test selection by JavaScript file extension"""
        selector = AdapterSelector()
        adapter = selector.select(file_path="test.js")
        assert adapter == "javascript_adapter"
    
    def test_select_by_project_structure_odoo(self):
        """Test selection by Odoo project structure"""
        selector = AdapterSelector()
        project_structure = {
            "path": "/path/to/odoo/project",
            "name": "odoo_project"
        }
        adapter = selector.select(project_structure=project_structure)
        assert adapter == "odoo_adapter"
    
    def test_select_by_project_structure_django(self):
        """Test selection by Django project structure"""
        selector = AdapterSelector()
        project_structure = {
            "path": "/path/to/django/project",
            "name": "django_project"
        }
        adapter = selector.select(project_structure=project_structure)
        assert adapter == "django_adapter"
    
    def test_select_fallback_generic(self):
        """Test fallback to generic adapter"""
        selector = AdapterSelector()
        adapter = selector.select(file_path="test.unknown")
        assert adapter == "generic_adapter"
    
    def test_select_priority_extension_over_structure(self):
        """Test that extension takes priority over project structure"""
        selector = AdapterSelector()
        adapter = selector.select(
            file_path="test.py",
            project_structure={"path": "/path/to/odoo"}
        )
        # Extension should take priority
        assert adapter == "python_adapter"

