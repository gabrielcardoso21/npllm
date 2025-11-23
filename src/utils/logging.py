"""
Logging configuration for npllm
Structured logging with JSON format support
"""

import sys
import json
from pathlib import Path
from typing import Any, Dict, Optional
from loguru import logger
from datetime import datetime


class StructuredLogger:
    """Structured logger wrapper around loguru"""
    
    def __init__(self, name: str, level: str = "INFO", log_file: Optional[str] = None):
        """
        Initialize structured logger
        
        Args:
            name: Logger name
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
        """
        self.name = name
        self.logger = logger.bind(name=name)
        
        # Remove default handler
        logger.remove()
        
        # Add console handler with structured format
        logger.add(
            sys.stderr,
            format=self._format_log,
            level=level,
            colorize=True
        )
        
        # Add file handler if specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            logger.add(
                log_file,
                format=self._format_log,
                level=level,
                rotation="10 MB",
                retention="7 days",
                compression="zip"
            )
    
    def _format_log(self, record: Dict[str, Any]) -> str:
        """Format log record as simple text (evita problemas com format_map)"""
        try:
            # Tenta acessar time do record
            time_obj = record.get("time")
            if time_obj:
                if hasattr(time_obj, "isoformat"):
                    timestamp = time_obj.isoformat()
                else:
                    timestamp = str(time_obj)
            else:
                timestamp = datetime.utcnow().isoformat()
        except:
            timestamp = datetime.utcnow().isoformat()
        
        level = record.get("level", {}).name if hasattr(record.get("level", {}), "name") else "INFO"
        message = record.get("message", "")
        module = record.get("name", "")
        function = record.get("function", "")
        line = record.get("line", 0)
        
        # Formato simples e legível (evita JSON para não ter problemas com format_map)
        return f"[{timestamp}] {level} | {self.name} | {module}:{function}:{line} | {message}"
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, **kwargs)


def get_logger(name: str, level: str = "INFO", log_file: Optional[str] = None) -> StructuredLogger:
    """
    Get logger instance
    
    Args:
        name: Logger name (usually module name)
        level: Log level
        log_file: Optional log file path
    
    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name, level, log_file)

