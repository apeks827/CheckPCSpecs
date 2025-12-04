"""Configuration management for CheckPCSpecs."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfig:
    """Application configuration."""
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # System checks thresholds
    min_ram_gb_good: float = 7.8
    min_ram_gb_acceptable: float = 5.8
    min_cpu_cores_good: int = 4
    min_cpu_threads_good: int = 4
    
    # Network checks thresholds
    min_download_mbps: float = 20.0
    min_upload_mbps: float = 10.0
    max_ping_ms_excellent: float = 30.0
    max_ping_ms_acceptable: float = 100.0
    
    # Speed test configuration
    speedtest_timeout: int = 60
    speedtest_retries: int = 3
    
    # Ping test configuration
    ping_host: str = "8.8.8.8"
    ping_count: int = 4
    ping_timeout: int = 5
    
    # UI configuration
    window_title: str = "CheckPCSpecs"
    window_width: int = 800
    window_height: int = 600
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create config from environment variables."""
        return cls(
            log_level=os.getenv("CHECKPCSPECS_LOG_LEVEL", "INFO"),
            log_file=os.getenv("CHECKPCSPECS_LOG_FILE"),
            min_ram_gb_good=float(os.getenv("CHECKPCSPECS_MIN_RAM_GOOD", "7.8")),
            min_download_mbps=float(os.getenv("CHECKPCSPECS_MIN_DOWNLOAD", "20.0")),
            ping_host=os.getenv("CHECKPCSPECS_PING_HOST", "8.8.8.8"),
        )
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "log_level": self.log_level,
            "min_ram_gb_good": self.min_ram_gb_good,
            "min_download_mbps": self.min_download_mbps,
            "ping_host": self.ping_host,
        }


# Global config instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = AppConfig.from_env()
    return _config


def set_config(config: AppConfig) -> None:
    """Set global configuration instance."""
    global _config
    _config = config
