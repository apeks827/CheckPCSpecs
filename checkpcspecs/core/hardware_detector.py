"""Hardware detection utilities."""

import platform
import logging
from typing import Optional, Tuple

import psutil
import cpuinfo

from checkpcspecs.exceptions import HardwareDetectionError

logger = logging.getLogger(__name__)


class HardwareDetector:
    """Detects and retrieves hardware information."""

    @staticmethod
    def get_os_info() -> Tuple[str, str]:
        """Get OS version and release.
        
        Returns:
            Tuple of (version, release)
            
        Raises:
            HardwareDetectionError: If OS info cannot be detected
        """
        try:
            system = platform.system()
            if system != "Windows":
                raise HardwareDetectionError(f"Unsupported OS: {system}")
            
            version = platform.version()
            release = platform.release()
            
            # Parse Windows version
            if "10." in version:
                # Windows 10/11
                build = version.split(".")[-1]
                if int(build) >= 22000:
                    return "11", version
                return "10", version
            elif "6.3" in version:
                return "8.1", version
            elif "6.2" in version:
                return "8", version
            elif "6.1" in version:
                return "7", version
            else:
                return release, version
                
        except Exception as e:
            logger.error(f"Failed to detect OS info: {e}")
            raise HardwareDetectionError(f"Cannot detect OS info: {e}")

    @staticmethod
    def get_architecture() -> str:
        """Get CPU architecture.
        
        Returns:
            'x64' or 'x32'
            
        Raises:
            HardwareDetectionError: If architecture cannot be detected
        """
        try:
            machine = platform.machine().lower()
            if 'amd64' in machine or 'x86_64' in machine:
                return 'x64'
            elif 'i386' in machine or 'i686' in machine or 'x86' in machine:
                return 'x32'
            else:
                logger.warning(f"Unknown architecture: {machine}, defaulting to x64")
                return 'x64'
        except Exception as e:
            logger.error(f"Failed to detect architecture: {e}")
            raise HardwareDetectionError(f"Cannot detect architecture: {e}")

    @staticmethod
    def get_ram_gb() -> float:
        """Get total RAM in GB.
        
        Returns:
            RAM size in GB
            
        Raises:
            HardwareDetectionError: If RAM cannot be detected
        """
        try:
            ram_bytes = psutil.virtual_memory().total
            ram_gb = round(ram_bytes / (1024 ** 3), 2)
            return ram_gb
        except Exception as e:
            logger.error(f"Failed to detect RAM: {e}")
            raise HardwareDetectionError(f"Cannot detect RAM: {e}")

    @staticmethod
    def get_cpu_info() -> Tuple[str, int, int]:
        """Get CPU information.
        
        Returns:
            Tuple of (brand, physical_cores, logical_cores)
            
        Raises:
            HardwareDetectionError: If CPU info cannot be detected
        """
        try:
            info = cpuinfo.get_cpu_info()
            brand = info.get('brand_raw', 'Unknown CPU')
            
            physical_cores = psutil.cpu_count(logical=False) or 1
            logical_cores = psutil.cpu_count(logical=True) or 1
            
            return brand, physical_cores, logical_cores
        except Exception as e:
            logger.error(f"Failed to detect CPU info: {e}")
            raise HardwareDetectionError(f"Cannot detect CPU info: {e}")

    @staticmethod
    def get_disk_type() -> str:
        """Get primary disk type.
        
        Returns:
            'SSD', 'NVME', 'HDD', or 'Unknown'
            
        Note:
            This is a best-effort detection. May not be 100% accurate.
        """
        try:
            # Try to detect using Windows WMI
            if platform.system() == "Windows":
                try:
                    import wmi
                    w = wmi.WMI()
                    for disk in w.Win32_DiskDrive():
                        model = disk.Model.upper()
                        media_type = str(disk.MediaType).upper() if disk.MediaType else ""
                        
                        # Check for NVMe
                        if 'NVME' in model or 'NVM' in model:
                            return 'NVME'
                        
                        # Check for SSD indicators
                        if 'SSD' in model or 'SOLID STATE' in media_type:
                            return 'SSD'
                        
                        # Check for HDD indicators
                        if 'HDD' in model or 'HARD DISK' in media_type:
                            return 'HDD'
                    
                    # If we can't determine, assume SSD for modern systems
                    logger.warning("Could not determine disk type, assuming SSD")
                    return 'SSD'
                except ImportError:
                    logger.warning("WMI not available, cannot detect disk type")
                    return 'Unknown'
                except Exception as e:
                    logger.warning(f"WMI detection failed: {e}")
                    return 'Unknown'
            else:
                return 'Unknown'
        except Exception as e:
            logger.error(f"Failed to detect disk type: {e}")
            return 'Unknown'
