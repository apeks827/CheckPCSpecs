"""Core domain models and business logic for CheckPCSpecs."""

from checkpcspecs.core.models import (
    PCCheckResult,
    SystemInfo,
    PerformanceMetrics,
    RequirementLevel,
    SystemComponentStatus,
)
from checkpcspecs.core.specs_checker import SpecsChecker
from checkpcspecs.core.result_models import (
    OSResult,
    ArchResult,
    RAMResult,
    CPUResult,
    DiskResult,
    NetworkResult,
)

__all__ = [
    # Models
    "PCCheckResult",
    "SystemInfo",
    "PerformanceMetrics",
    "RequirementLevel",
    "SystemComponentStatus",
    # Checker
    "SpecsChecker",
    # Result wrappers (backwards compatibility)
    "OSResult",
    "ArchResult",
    "RAMResult",
    "CPUResult",
    "DiskResult",
    "NetworkResult",
]
