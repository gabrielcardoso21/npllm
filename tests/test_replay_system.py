"""
Tests for Replay System
TDD: Tests first
"""

import pytest
from src.learning.replay import ReplaySystem


class TestReplaySystem:
    """Test suite for ReplaySystem"""
    
    def test_replay_initialization(self):
        """Test replay system initialization"""
        replay = ReplaySystem(replay_ratio=0.3)
        assert replay is not None
        assert replay.replay_ratio == 0.3
    
    def test_mix_examples_only_new(self):
        """Test mixing when only new examples exist"""
        replay = ReplaySystem()
        new_examples = [
            {"score": 0.8, "prompt": "test1"},
            {"score": 0.9, "prompt": "test2"}
        ]
        
        result = replay.mix_examples([], new_examples)
        assert len(result) == 2
        assert result == new_examples
    
    def test_mix_examples_only_old(self):
        """Test mixing when only old examples exist"""
        replay = ReplaySystem()
        old_examples = [
            {"score": 0.7, "prompt": "old1"},
            {"score": 0.8, "prompt": "old2"}
        ]
        
        result = replay.mix_examples(old_examples, [])
        assert len(result) == 2
        assert result == old_examples
    
    def test_mix_examples_both(self):
        """Test mixing when both old and new examples exist"""
        replay = ReplaySystem(replay_ratio=0.3)
        old_examples = [
            {"score": 0.9, "prompt": "old1"},
            {"score": 0.8, "prompt": "old2"},
            {"score": 0.7, "prompt": "old3"}
        ]
        new_examples = [
            {"score": 0.85, "prompt": "new1"},
            {"score": 0.9, "prompt": "new2"},
            {"score": 0.95, "prompt": "new3"}
        ]
        
        result = replay.mix_examples(old_examples, new_examples)
        # Should have new examples + some old examples
        assert len(result) >= len(new_examples)
    
    def test_prioritize_by_satisfaction(self):
        """Test prioritization by satisfaction score"""
        replay = ReplaySystem()
        examples = [
            {"score": 0.5, "prompt": "low"},
            {"score": 0.9, "prompt": "high"},
            {"score": 0.7, "prompt": "medium"}
        ]
        
        result = replay.prioritize_by_satisfaction(examples)
        assert result[0]["score"] == 0.9  # Highest first
        assert result[-1]["score"] == 0.5  # Lowest last

