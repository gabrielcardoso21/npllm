"""
Unit tests for code chunking
"""

import pytest
from pathlib import Path
import tempfile

from src.rag.chunking import CodeChunker


def test_chunk_python():
    """Test Python code chunking"""
    chunker = CodeChunker()
    
    code = """
def hello():
    print("Hello")
    
class Test:
    def method(self):
        pass
"""
    
    chunks = chunker.chunk_python(code, "test.py")
    assert len(chunks) > 0
    assert any(chunk["metadata"]["type"] == "function" for chunk in chunks)
    assert any(chunk["metadata"]["type"] == "class" for chunk in chunks)


def test_chunk_javascript():
    """Test JavaScript code chunking"""
    chunker = CodeChunker()
    
    code = """
function hello() {
    console.log("Hello");
}

class Test {
    method() {
        return true;
    }
}
"""
    
    chunks = chunker.chunk_javascript(code, "test.js")
    assert len(chunks) > 0

