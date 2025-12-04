"""CheckPCSpecs - Professional PC System Requirements Checker

A comprehensive system diagnostics tool that checks PC specifications
against requirements and provides real-time performance metrics.

Version: 2.0.0 - Architecture Refactored
Author: apeks827
"""

__version__ = "2.0.0"
__author__ = "apeks827"

from checkpcspecs.core.models import PCCheckResult, SystemInfo, PerformanceMetrics
from checkpcspecs.core.specs_checker import SpecsChecker
from checkpcspecs.infrastructure.system_info import SystemInfoCollector
from checkpcspecs.infrastructure.network import NetworkDiagnostics

__all__ = [
    "SpecsChecker",
    "PCCheckResult",
    "SystemInfo",
    "PerformanceMetrics",
    "SystemInfoCollector",
    "NetworkDiagnostics",
]
