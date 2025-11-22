"""
Tests for Sleep System
TDD: Tests first
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timedelta
from src.learning.sleep import SleepSystem


class TestSleepSystem:
    """Test suite for SleepSystem"""
    
    def test_sleep_initialization(self):
        """Test sleep system initialization"""
        mock_storage = Mock()
        mock_replay = Mock()
        mock_fine_tuning = Mock()
        
        sleep = SleepSystem(
            storage=mock_storage,
            replay=mock_replay,
            fine_tuning=mock_fine_tuning,
            inactivity_threshold_minutes=30
        )
        
        assert sleep is not None
        assert sleep.inactivity_threshold == timedelta(minutes=30)
    
    def test_record_activity(self):
        """Test activity recording"""
        mock_storage = Mock()
        mock_replay = Mock()
        mock_fine_tuning = Mock()
        
        sleep = SleepSystem(mock_storage, mock_replay, mock_fine_tuning)
        sleep.record_activity()
        
        assert sleep.last_activity is not None
        assert isinstance(sleep.last_activity, datetime)
    
    def test_is_inactive_false_when_active(self):
        """Test inactivity detection when system is active"""
        mock_storage = Mock()
        mock_replay = Mock()
        mock_fine_tuning = Mock()
        
        sleep = SleepSystem(mock_storage, mock_replay, mock_fine_tuning)
        sleep.record_activity()
        
        # Just recorded activity, should not be inactive
        assert sleep.is_inactive() is False
    
    def test_consolidate_when_active(self):
        """Test consolidation when system is still active"""
        mock_storage = Mock()
        mock_replay = Mock()
        mock_fine_tuning = Mock()
        
        sleep = SleepSystem(mock_storage, mock_replay, mock_fine_tuning)
        sleep.record_activity()
        
        result = sleep.consolidate()
        assert result["status"] == "active"

