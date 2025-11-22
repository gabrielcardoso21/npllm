"""
Pytest configuration and fixtures
"""

import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path


@pytest.fixture
def mock_logger():
    """Mock logger"""
    return MagicMock()


@pytest.fixture
def mock_config():
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
    return config


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for tests"""
    return tmp_path

