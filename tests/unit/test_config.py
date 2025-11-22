"""
Unit tests for configuration management
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from src.utils.config import Config, get_config


def test_config_load():
    """Test loading configuration"""
    config = get_config()
    assert config is not None
    assert config.get("model.base_model") is not None


def test_config_sections():
    """Test configuration sections"""
    config = get_config()
    
    assert config.database is not None
    assert config.model is not None
    assert config.rag is not None


def test_config_env_override():
    """Test environment variable override"""
    import os
    
    original_value = os.getenv("DB_HOST")
    os.environ["DB_HOST"] = "test_host"
    
    try:
        config = Config()  # New instance to pick up env var
        assert config.database.host == "test_host"
    finally:
        if original_value:
            os.environ["DB_HOST"] = original_value
        else:
            del os.environ["DB_HOST"]

