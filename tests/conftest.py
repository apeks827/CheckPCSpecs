"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock, MagicMock
from checkpcspecs.core.models import SystemInfo, PerformanceMetrics, SystemComponentStatus
from datetime import datetime


@pytest.fixture
def mock_system_info():
    """Fixture providing mock system information."""
    return SystemInfo(
        os_version="10",
        os_release="10.0.22000",
        architecture="x64",
        cpu_brand="Intel Core i7-9700K",
        cpu_cores=8,
        cpu_threads=8,
        ram_gb=16.0,
        disk_type="SSD",
        timestamp=datetime.now()
    )


@pytest.fixture
def mock_performance_metrics():
    """Fixture providing mock performance metrics."""
    return PerformanceMetrics(
        download_mbps=100.0,
        upload_mbps=50.0,
        ping_ms=20.0,
        status=SystemComponentStatus.EXCELLENT
    )


@pytest.fixture
def mock_low_spec_system():
    """Fixture providing low-spec system information."""
    return SystemInfo(
        os_version="7",
        os_release="6.1.7601",
        architecture="x32",
        cpu_brand="Intel Atom Z3735F",
        cpu_cores=2,
        cpu_threads=2,
        ram_gb=4.0,
        disk_type="HDD",
        timestamp=datetime.now()
    )


@pytest.fixture
def mock_high_spec_system():
    """Fixture providing high-spec system information."""
    return SystemInfo(
        os_version="11",
        os_release="10.0.22621",
        architecture="x64",
        cpu_brand="AMD Ryzen 9 5950X",
        cpu_cores=16,
        cpu_threads=32,
        ram_gb=32.0,
        disk_type="NVME",
        timestamp=datetime.now()
    )
