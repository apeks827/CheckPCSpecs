"""Result models for PC component checks.

These models provide backwards compatibility with the old API.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OSResult:
    """Result of OS check."""
    version: str
    release: str
    rating: int  # 2=Win11, 1=Win10, 0=Win8, -1=Win7 or below
    score: int


@dataclass
class ArchResult:
    """Result of architecture check."""
    architecture: str
    rating: int  # 1=x64, -1=x32
    score: int


@dataclass
class RAMResult:
    """Result of RAM check."""
    total_gb: float
    rating: int  # 1=excellent, 0=good, -1=poor
    score: int


@dataclass
class CPUResult:
    """Result of CPU check."""
    name: str
    cores: int
    threads: int
    rating: int  # 1=excellent, 0=good, -1=poor
    score: int


@dataclass
class DiskResult:
    """Result of disk check."""
    disk_type: str
    rating: int  # 1=SSD, 0=HDD (good RAM), -1=HDD (low RAM), -2=unknown
    score: int


@dataclass
class NetworkResult:
    """Result of network check."""
    download: float
    upload: float
    ping: Optional[float]
    rating: int
    score: int
