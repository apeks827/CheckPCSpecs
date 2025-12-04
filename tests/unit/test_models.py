"""Unit tests for core models."""

import pytest
from datetime import datetime
from checkpcspecs.core.models import (
    SystemInfo,
    PerformanceMetrics,
    PCCheckResult,
    SystemComponentStatus,
    RequirementLevel
)


class TestSystemInfo:
    """Test SystemInfo model."""

    def test_creation(self):
        """Test SystemInfo instance creation."""
        info = SystemInfo(
            os_version="10",
            os_release="10.0.22000",
            architecture="x64",
            cpu_brand="Intel Core i7",
            cpu_cores=8,
            cpu_threads=16,
            ram_gb=16.0,
            disk_type="SSD"
        )
        assert info.os_version == "10"
        assert info.architecture == "x64"
        assert info.cpu_cores == 8
        assert isinstance(info.timestamp, datetime)

    def test_to_dict(self, mock_system_info):
        """Test SystemInfo serialization to dict."""
        data = mock_system_info.to_dict()
        assert isinstance(data, dict)
        assert data["os_version"] == "10"
        assert data["cpu_cores"] == 8
        assert "timestamp" in data


class TestPerformanceMetrics:
    """Test PerformanceMetrics model."""

    def test_creation(self):
        """Test PerformanceMetrics creation."""
        metrics = PerformanceMetrics(
            download_mbps=100.0,
            upload_mbps=50.0,
            ping_ms=20.0
        )
        assert metrics.download_mbps == 100.0
        assert metrics.upload_mbps == 50.0
        assert metrics.ping_ms == 20.0

    def test_optional_ping(self):
        """Test PerformanceMetrics with optional ping."""
        metrics = PerformanceMetrics(
            download_mbps=100.0,
            upload_mbps=50.0
        )
        assert metrics.ping_ms is None

    def test_to_dict(self, mock_performance_metrics):
        """Test PerformanceMetrics serialization."""
        data = mock_performance_metrics.to_dict()
        assert isinstance(data, dict)
        assert "download_mbps" in data
        assert "status" in data


class TestSystemComponentStatus:
    """Test SystemComponentStatus enum."""

    def test_enum_values(self):
        """Test all enum values exist."""
        assert SystemComponentStatus.EXCELLENT.value == "excellent"
        assert SystemComponentStatus.GOOD.value == "good"
        assert SystemComponentStatus.POOR.value == "poor"
        assert SystemComponentStatus.UNKNOWN.value == "unknown"


class TestRequirementLevel:
    """Test RequirementLevel enum."""

    def test_enum_values(self):
        """Test all enum values exist."""
        assert RequirementLevel.EXCEEDS.value == "exceeds"
        assert RequirementLevel.MEETS.value == "meets"
        assert RequirementLevel.MINIMUM.value == "minimum"
        assert RequirementLevel.BELOW.value == "below"
