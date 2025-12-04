"""Unit tests for network testing modules."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from checkpcspecs.network.evaluator import NetworkEvaluator
from checkpcspecs.network.ping import PingTester, PingResult
from checkpcspecs.network.speedtest import SpeedTester, SpeedTestResult


class TestNetworkEvaluator:
    """Test NetworkEvaluator."""

    def test_evaluate_excellent(self):
        """Test evaluation of excellent network."""
        result = NetworkEvaluator.evaluate(100.0, 50.0, 20.0)
        assert result.score_points == 5
        assert result.status_text == "отличное"

    def test_evaluate_good(self):
        """Test evaluation of good network."""
        result = NetworkEvaluator.evaluate(50.0, 20.0, 50.0)
        assert result.score_points == 2
        assert result.status_text == "хорошее"

    def test_evaluate_poor(self):
        """Test evaluation of poor network."""
        result = NetworkEvaluator.evaluate(10.0, 5.0, 150.0)
        assert result.score_points == -999
        assert result.status_text == "плохое"

    def test_evaluate_no_ping(self):
        """Test evaluation without ping data."""
        result = NetworkEvaluator.evaluate(100.0, 50.0, None)
        assert result.score_points == 5


class TestPingTester:
    """Test PingTester."""

    @patch('checkpcspecs.network.ping.ping')
    def test_successful_ping(self, mock_ping):
        """Test successful ping operation."""
        mock_host = Mock()
        mock_host.avg_rtt = 25.5
        mock_ping.return_value = mock_host

        result = PingTester.test()

        assert result.success is True
        assert result.latency == 25.5
        assert result.error is None

    @patch('checkpcspecs.network.ping.ping')
    def test_failed_ping(self, mock_ping):
        """Test failed ping operation."""
        mock_ping.side_effect = Exception("Network error")

        result = PingTester.test()

        assert result.success is False
        assert result.latency == 999.0
        assert "Network error" in result.error

    @patch('checkpcspecs.network.ping.ping')
    def test_ping_custom_host(self, mock_ping):
        """Test ping with custom host."""
        mock_host = Mock()
        mock_host.avg_rtt = 30.0
        mock_ping.return_value = mock_host

        result = PingTester.test(host="custom.host")

        assert result.success is True
        mock_ping.assert_called_once()


class TestSpeedTester:
    """Test SpeedTester."""

    @patch('checkpcspecs.network.speedtest.speedtest.Speedtest')
    def test_successful_speedtest(self, mock_speedtest_class):
        """Test successful speed test."""
        mock_st = Mock()
        mock_st.download.return_value = 100_000_000  # 100 Mbps in bits
        mock_st.upload.return_value = 50_000_000    # 50 Mbps in bits
        mock_speedtest_class.return_value = mock_st

        result = SpeedTester.test()

        assert result.success is True
        assert result.download == 100.0
        assert result.upload == 50.0
        assert result.error is None

    @patch('checkpcspecs.network.speedtest.speedtest.Speedtest')
    def test_failed_speedtest(self, mock_speedtest_class):
        """Test failed speed test."""
        mock_speedtest_class.side_effect = Exception("Connection timeout")

        result = SpeedTester.test()

        assert result.success is False
        assert result.download == 0.0
        assert result.upload == 0.0
        assert "Connection timeout" in result.error

    @patch('checkpcspecs.network.speedtest.speedtest.Speedtest')
    def test_speedtest_conversion(self, mock_speedtest_class):
        """Test speed conversion from bits to Mbps."""
        mock_st = Mock()
        mock_st.download.return_value = 50_000_000   # 50 Mbps
        mock_st.upload.return_value = 10_000_000     # 10 Mbps
        mock_speedtest_class.return_value = mock_st

        result = SpeedTester.test()

        assert result.download == 50.0
        assert result.upload == 10.0
