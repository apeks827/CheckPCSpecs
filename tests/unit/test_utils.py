"""Unit tests for utility functions."""

import pytest
from unittest.mock import Mock, patch
from checkpcspecs.utils import ScoreCalculator


class TestScoreCalculator:
    """Test ScoreCalculator utility."""

    def test_calculate_excellent_score(self):
        """Test calculation for excellent PC."""
        # All excellent: 5, 2, 5, 5, 5 = 22
        result = ScoreCalculator.calculate(5, 2, 5, 5, 5, 5)
        assert result.total_score >= 18
        assert result.verdict_text_ru == "ПК отлично подходит для работы"
        assert result.verdict_color == "green"

    def test_calculate_good_score(self):
        """Test calculation for good PC."""
        # Mixed: 2, 2, 2, 2, 2, 2 = 12
        result = ScoreCalculator.calculate(2, 2, 2, 2, 2, 2)
        assert 10 <= result.total_score < 18
        assert result.verdict_text_ru == "ПК подходит для работы"
        assert result.verdict_color == "blue"

    def test_calculate_minimum_score(self):
        """Test calculation for minimum PC."""
        # Low scores: 2, 2, 0, 2, 0, 0 = 6
        result = ScoreCalculator.calculate(2, 2, 0, 2, 0, 0)
        assert 0 <= result.total_score < 10
        assert "подходит минимально" in result.verdict_text_ru.lower()
        assert result.verdict_color == "orange"

    def test_calculate_poor_score(self):
        """Test calculation for poor PC."""
        # Poor scores: -999, 0, 0, 0, 0, 0 = -999
        result = ScoreCalculator.calculate(-999, 0, 0, 0, 0, 0)
        assert result.total_score < 0
        assert "не подходит" in result.verdict_text_ru.lower()
        assert result.verdict_color == "red"

    def test_calculate_with_network_bonus(self):
        """Test calculation including network score."""
        # With network: 5, 2, 5, 5, 5, 5 = 27
        result = ScoreCalculator.calculate(5, 2, 5, 5, 5, 5)
        assert result.total_score >= 22

    def test_calculate_minimum_capped_score(self):
        """Test that score is capped at minimum -999."""
        # Multiple poor components
        result = ScoreCalculator.calculate(-999, -999, -999, -999, -999, -999)
        assert result.total_score == -999
