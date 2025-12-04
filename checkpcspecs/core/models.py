"""Domain models for PC system specifications and diagnostics."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class RequirementLevel(str, Enum):
  """Enumeration of PC requirement levels."""
  EXCEEDS = "exceeds"  # Exceeds requirements
  MEETS = "meets"      # Meets requirements
  MINIMUM = "minimum"  # Meets minimum requirements
  BELOW = "below"      # Below requirements


class SystemComponentStatus(str, Enum):
  """Status of individual system components."""
  EXCELLENT = "excellent"  # 5 - excellent
  GOOD = "good"            # 2-4 - acceptable
  POOR = "poor"            # 1 - poor
  UNKNOWN = "unknown"      # -1 or -2 - unable to determine


@dataclass
class SystemInfo:
  """Complete system information."""
  os_version: str
  os_release: str
  architecture: str  # x64, x32
  cpu_brand: str
  cpu_cores: int
  cpu_threads: int
  ram_gb: float
  disk_type: str  # SSD, HDD, eMMC
  timestamp: datetime = field(default_factory=datetime.now)

  def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary representation."""
    return {
        "os_version": self.os_version,
        "os_release": self.os_release,
        "architecture": self.architecture,
        "cpu_brand": self.cpu_brand,
        "cpu_cores": self.cpu_cores,
        "cpu_threads": self.cpu_threads,
        "ram_gb": self.ram_gb,
        "disk_type": self.disk_type,
        "timestamp": self.timestamp.isoformat(),
    }


@dataclass
class PerformanceMetrics:
  """Network and performance metrics."""
  download_mbps: float
  upload_mbps: float
  ping_ms: Optional[float] = None
  status: SystemComponentStatus = SystemComponentStatus.UNKNOWN
  error_message: Optional[str] = None

  def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary representation."""
    return {
        "download_mbps": self.download_mbps,
        "upload_mbps": self.upload_mbps,
        "ping_ms": self.ping_ms,
        "status": self.status.value,
        "error_message": self.error_message,
    }


@dataclass
class PCCheckResult:
  """Complete PC system check result."""
  user_name: str
  system_info: SystemInfo
  performance_metrics: PerformanceMetrics
  os_level: SystemComponentStatus
  architecture_level: SystemComponentStatus
  ram_level: SystemComponentStatus
  cpu_level: SystemComponentStatus
  disk_level: SystemComponentStatus
  overall_score: int
  requirement_level: RequirementLevel
  timestamp: datetime = field(default_factory=datetime.now)
  details: Dict[str, Any] = field(default_factory=dict)

  def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary representation."""
    return {
        "user_name": self.user_name,
        "system_info": self.system_info.to_dict(),
        "performance_metrics": self.performance_metrics.to_dict(),
        "component_status": {
            "os": self.os_level.value,
            "architecture": self.architecture_level.value,
            "ram": self.ram_level.value,
            "cpu": self.cpu_level.value,
            "disk": self.disk_level.value,
        },
        "overall_score": self.overall_score,
        "requirement_level": self.requirement_level.value,
        "timestamp": self.timestamp.isoformat(),
        "details": self.details,
    }

  def __str__(self) -> str:
    """Human-readable representation."""
    return f"PC Check for {self.user_name}: {self.requirement_level.value.upper()}"
