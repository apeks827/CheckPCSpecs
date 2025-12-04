"""PC specifications checker - core business logic."""

from typing import Optional
from logging import getLogger

from checkpcspecs.core.models import (
    PCCheckResult, SystemInfo, PerformanceMetrics,
    RequirementLevel, SystemComponentStatus
)

logger = getLogger(__name__)


class SpecsChecker:
  """Evaluates PC specs against requirements."""

  # Thresholds for evaluation
  MIN_RAM_GB_GOOD = 7.8
  MIN_RAM_GB_ACCEPTABLE = 5.8
  MIN_CPU_CORES_GOOD = 4
  MIN_CPU_THREADS_GOOD = 4
  MIN_DOWNLOAD_MBPS = 20
  MIN_UPLOAD_MBPS = 10
  MAX_PING_MS_EXCELLENT = 30
  MAX_PING_MS_ACCEPTABLE = 100

  BAD_CPU_MARKERS = {'atom', 'duo', 'quad', 'dualcore', 'sempron'}

  def evaluate_os(self, os_version: str, os_release: str) -> SystemComponentStatus:
    """Evaluate OS version."""
    try:
      if os_version == "10":
        release_int = int(os_release.replace(".", ""))
        if release_int >= 10022000:
          return SystemComponentStatus.GOOD
        return SystemComponentStatus.GOOD
      elif os_version in ["8", "8.1", "7"]:
        return SystemComponentStatus.POOR
      return SystemComponentStatus.UNKNOWN
    except Exception as e:
      logger.error(f"Error evaluating OS: {e}")
      return SystemComponentStatus.UNKNOWN

  def evaluate_architecture(self, architecture: str) -> SystemComponentStatus:
    """Evaluate CPU architecture."""
    return (
        SystemComponentStatus.GOOD if architecture == "x64"
        else SystemComponentStatus.POOR
    )

  def evaluate_ram(self, ram_gb: float) -> SystemComponentStatus:
    """Evaluate RAM amount."""
    if ram_gb >= self.MIN_RAM_GB_GOOD:
      return SystemComponentStatus.EXCELLENT
    elif ram_gb >= self.MIN_RAM_GB_ACCEPTABLE:
      return SystemComponentStatus.GOOD
    else:
      return SystemComponentStatus.POOR

  def evaluate_cpu(self, cpu_brand: str, cores: int, threads: int) -> SystemComponentStatus:
    """Evaluate CPU specifications."""
    brand_lower = cpu_brand.lower().replace(" ", "").replace("-", "")
    if any(marker in brand_lower for marker in self.BAD_CPU_MARKERS):
      return SystemComponentStatus.POOR
    if cores >= self.MIN_CPU_CORES_GOOD and threads >= self.MIN_CPU_THREADS_GOOD:
      return SystemComponentStatus.EXCELLENT
    elif cores >= 2 and threads >= 4:
      return SystemComponentStatus.GOOD
    return SystemComponentStatus.POOR

  def evaluate_disk(self, disk_type: str, ram_gb: float) -> SystemComponentStatus:
    """Evaluate disk type and configuration."""
    is_ssd = disk_type.upper() in ["SSD", "NVME"]
    if is_ssd:
      if 3.8 <= ram_gb < 5.8:
        return SystemComponentStatus.GOOD
      return SystemComponentStatus.EXCELLENT
    elif ram_gb >= 7.8:
      return SystemComponentStatus.GOOD
    else:
      return SystemComponentStatus.POOR

  def evaluate_network(self, download: float, upload: float,
                       ping: Optional[float] = None) -> SystemComponentStatus:
    """Evaluate network performance."""
    if download >= self.MIN_DOWNLOAD_MBPS and upload >= self.MIN_UPLOAD_MBPS:
      if ping is None or ping <= self.MAX_PING_MS_EXCELLENT:
        return SystemComponentStatus.EXCELLENT
      elif ping <= self.MAX_PING_MS_ACCEPTABLE:
        return SystemComponentStatus.GOOD
      return SystemComponentStatus.GOOD
    return SystemComponentStatus.POOR

  def calculate_overall_score(self, os: SystemComponentStatus,
                             arch: SystemComponentStatus,
                             ram: SystemComponentStatus,
                             cpu: SystemComponentStatus,
                             disk: SystemComponentStatus) -> int:
    """Calculate overall PC score."""
    score_map = {
        SystemComponentStatus.EXCELLENT: 5,
        SystemComponentStatus.GOOD: 2,
        SystemComponentStatus.POOR: -999,
        SystemComponentStatus.UNKNOWN: 0,
    }
    total = sum(score_map.get(status, 0) for status in
                [os, arch, ram, cpu, disk])
    return max(total, -999)  # Minimum score

  def determine_requirement_level(self, score: int) -> RequirementLevel:
    """Determine overall requirement level from score."""
    if score >= 18:
      return RequirementLevel.EXCEEDS
    elif score >= 10:
      return RequirementLevel.MEETS
    elif score >= 0:
      return RequirementLevel.MINIMUM
    return RequirementLevel.BELOW
