"""
Configuration management for npllm
Supports YAML configuration files with environment variable overrides
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class DatabaseConfig(BaseSettings):
    """Database configuration"""
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    database: str = Field(default="npllm", env="DB_NAME")
    user: str = Field(default="npllm_user", env="DB_USER")
    password: str = Field(default="", env="DB_PASSWORD")
    pool_size: int = 5
    max_overflow: int = 10
    shared_buffers: str = "256MB"
    effective_cache_size: str = "1GB"
    work_mem: str = "16MB"
    maintenance_work_mem: str = "128MB"


class ModelConfig(BaseSettings):
    """Model configuration"""
    base_model: str = "codellama/CodeLlama-3B-Instruct"
    quantization: str = "4bit"
    quantization_type: str = "ggml"
    device: str = "cpu"
    max_memory: str = "6GB"


class RAGConfig(BaseSettings):
    """RAG configuration (optimized: on-demand)"""
    enabled: bool = True
    on_demand: bool = True  # Only activate when context is insufficient
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5
    similarity_threshold: float = 0.7


class Config:
    """Main configuration class"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to YAML config file. If None, uses default.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "default.yaml"
        
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)
        
        # Override with environment variables
        self._override_with_env()
    
    def _override_with_env(self):
        """Override config values with environment variables"""
        # Database config
        if os.getenv("DB_HOST"):
            self._config.setdefault("database", {})["host"] = os.getenv("DB_HOST")
        if os.getenv("DB_PORT"):
            self._config.setdefault("database", {})["port"] = int(os.getenv("DB_PORT"))
        if os.getenv("DB_NAME"):
            self._config.setdefault("database", {})["database"] = os.getenv("DB_NAME")
        if os.getenv("DB_USER"):
            self._config.setdefault("database", {})["user"] = os.getenv("DB_USER")
        if os.getenv("DB_PASSWORD"):
            self._config.setdefault("database", {})["password"] = os.getenv("DB_PASSWORD")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self._config.get(section, {})
    
    @property
    def database(self) -> DatabaseConfig:
        """Get database configuration"""
        db_config = self.get_section("database")
        return DatabaseConfig(**db_config)
    
    @property
    def model(self) -> ModelConfig:
        """Get model configuration"""
        model_config = self.get_section("model")
        return ModelConfig(**model_config)
    
    @property
    def rag(self) -> RAGConfig:
        """Get RAG configuration"""
        rag_config = self.get_section("rag")
        return RAGConfig(**rag_config)


# Global config instance
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance

