"""Backwards compatible wrapper for SpecsChecker.

This provides the old API that returns result objects instead of tuples.
"""

import asyncio
import logging
import platform

import psutil
import cpuinfo

from checkpcspecs.core.result_models import (
    OSResult,
    ArchResult,
    RAMResult,
    CPUResult,
    DiskResult,
)
from checkpcspecs.core.specs_checker import SpecsChecker as NewSpecsChecker
from checkpcspecs.core.models import SystemComponentStatus

logger = logging.getLogger(__name__)


class SpecsChecker(NewSpecsChecker):
    """Backwards compatible SpecsChecker.
    
    Wraps the new SpecsChecker to provide old API compatibility.
    """

    def check_os(self) -> OSResult:
        """Check operating system.
        
        Returns:
            OSResult with version, release, rating, and score
        """
        try:
            # Get OS info
            system = platform.system()
            if system != "Windows":
                return OSResult(
                    version="Unknown",
                    release="Unknown",
                    rating=-1,
                    score=-999
                )
            
            version = platform.version()
            release = platform.release()
            
            # Determine version
            if "10." in version:
                build = version.split(".")[-1]
                if int(build) >= 22000:
                    os_version = "11"
                    rating = 2
                else:
                    os_version = "10"
                    rating = 1
            elif "6.3" in version:
                os_version = "8.1"
                rating = 0
            elif "6.2" in version:
                os_version = "8"
                rating = 0
            elif "6.1" in version:
                os_version = "7"
                rating = -1
            else:
                os_version = release
                rating = 0
            
            # Calculate score
            status = self.evaluate_os(os_version, version)
            score = self._status_to_score(status)
            
            return OSResult(
                version=os_version,
                release=version,
                rating=rating,
                score=score
            )
        except Exception as e:
            logger.error(f"Error checking OS: {e}")
            return OSResult(
                version="Unknown",
                release="Unknown",
                rating=-1,
                score=-999
            )

    def check_architecture(self) -> ArchResult:
        """Check CPU architecture.
        
        Returns:
            ArchResult with architecture, rating, and score
        """
        try:
            machine = platform.machine().lower()
            if 'amd64' in machine or 'x86_64' in machine:
                arch = 'x64'
                rating = 1
            elif 'i386' in machine or 'i686' in machine or 'x86' in machine:
                arch = 'x32'
                rating = -1
            else:
                arch = 'x64'
                rating = 1
            
            status = self.evaluate_architecture(arch)
            score = self._status_to_score(status)
            
            return ArchResult(
                architecture=arch,
                rating=rating,
                score=score
            )
        except Exception as e:
            logger.error(f"Error checking architecture: {e}")
            return ArchResult(
                architecture="Unknown",
                rating=-1,
                score=-999
            )

    def check_ram(self) -> RAMResult:
        """Check RAM.
        
        Returns:
            RAMResult with total_gb, rating, and score
        """
        try:
            ram_bytes = psutil.virtual_memory().total
            ram_gb = round(ram_bytes / (1024 ** 3), 2)
            
            status = self.evaluate_ram(ram_gb)
            score = self._status_to_score(status)
            
            # Map status to rating
            if status == SystemComponentStatus.EXCELLENT:
                rating = 1
            elif status == SystemComponentStatus.GOOD:
                rating = 0
            else:
                rating = -1
            
            return RAMResult(
                total_gb=ram_gb,
                rating=rating,
                score=score
            )
        except Exception as e:
            logger.error(f"Error checking RAM: {e}")
            return RAMResult(
                total_gb=0.0,
                rating=-1,
                score=-999
            )

    def check_cpu(self) -> CPUResult:
        """Check CPU.
        
        Returns:
            CPUResult with name, cores, threads, rating, and score
        """
        try:
            info = cpuinfo.get_cpu_info()
            brand = info.get('brand_raw', 'Unknown CPU')
            
            physical_cores = psutil.cpu_count(logical=False) or 1
            logical_cores = psutil.cpu_count(logical=True) or 1
            
            status = self.evaluate_cpu(brand, physical_cores, logical_cores)
            score = self._status_to_score(status)
            
            # Map status to rating
            if status == SystemComponentStatus.EXCELLENT:
                rating = 1
            elif status == SystemComponentStatus.GOOD:
                rating = 0
            else:
                rating = -1
            
            return CPUResult(
                name=brand,
                cores=physical_cores,
                threads=logical_cores,
                rating=rating,
                score=score
            )
        except Exception as e:
            logger.error(f"Error checking CPU: {e}")
            return CPUResult(
                name="Unknown",
                cores=0,
                threads=0,
                rating=-1,
                score=-999
            )

    async def check_disk_async(self) -> DiskResult:
        """Check disk type (async).
        
        Returns:
            DiskResult with disk_type, rating, and score
        """
        try:
            # Run detection in thread pool
            disk_type = await asyncio.to_thread(self._detect_disk_type)
            ram_gb = psutil.virtual_memory().total / (1024 ** 3)
            
            status = self.evaluate_disk(disk_type, ram_gb)
            score = self._status_to_score(status)
            
            # Map to rating
            if disk_type == "Unknown":
                rating = -2
            elif disk_type.upper() in ["SSD", "NVME"]:
                rating = 1
            elif ram_gb >= 7.8:
                rating = 0
            else:
                rating = -1
            
            return DiskResult(
                disk_type=disk_type,
                rating=rating,
                score=score
            )
        except Exception as e:
            logger.error(f"Error checking disk: {e}")
            return DiskResult(
                disk_type="Unknown",
                rating=-2,
                score=0
            )

    def _detect_disk_type(self) -> str:
        """Detect disk type."""
        try:
            if platform.system() == "Windows":
                import wmi
                w = wmi.WMI()
                for disk in w.Win32_DiskDrive():
                    model = disk.Model.upper()
                    media_type = str(disk.MediaType).upper() if disk.MediaType else ""
                    
                    if 'NVME' in model or 'NVM' in model:
                        return 'NVME'
                    if 'SSD' in model or 'SOLID STATE' in media_type:
                        return 'SSD'
                    if 'HDD' in model or 'HARD DISK' in media_type:
                        return 'HDD'
                
                return 'SSD'  # Default assumption
            else:
                return 'Unknown'
        except Exception as e:
            logger.warning(f"Could not detect disk type: {e}")
            return 'Unknown'

    def _status_to_score(self, status: SystemComponentStatus) -> int:
        """Convert SystemComponentStatus to score."""
        score_map = {
            SystemComponentStatus.EXCELLENT: 5,
            SystemComponentStatus.GOOD: 2,
            SystemComponentStatus.POOR: -999,
            SystemComponentStatus.UNKNOWN: 0,
        }
        return score_map.get(status, 0)
