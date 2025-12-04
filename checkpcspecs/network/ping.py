"""Ping test functionality."""

import logging
from dataclasses import dataclass
from typing import Optional

from icmplib import ping as icmp_ping
from icmplib.exceptions import ICMPLibError

logger = logging.getLogger(__name__)


@dataclass
class PingResult:
    """Result of a ping test."""
    latency: float  # milliseconds
    success: bool
    error: Optional[str] = None


class PingTester:
    """Handles ping testing to measure network latency."""

    DEFAULT_HOSTS = [
        'ya.ru',
        '8.8.8.8',
        '1.1.1.1'
    ]

    @classmethod
    def test(cls, host: Optional[str] = None, count: int = 4) -> PingResult:
        """Perform ping test to measure latency.
        
        Args:
            host: Target host (default: tries multiple hosts)
            count: Number of ping attempts
            
        Returns:
            PingResult with average latency in milliseconds
        """
        hosts = [host] if host else cls.DEFAULT_HOSTS

        for target in hosts:
            try:
                logger.info(f"Pinging {target}...")
                result = icmp_ping(target, count=count, privileged=False)
                
                if result.is_alive:
                    latency = round(result.avg_rtt, 2)
                    logger.info(f"Ping successful: {latency} ms to {target}")
                    return PingResult(
                        latency=latency,
                        success=True
                    )
            except ICMPLibError as e:
                logger.warning(f"Ping to {target} failed: {e}")
                continue
            except Exception as e:
                logger.warning(f"Unexpected error pinging {target}: {e}")
                continue

        error_msg = "All ping attempts failed. Try running as administrator."
        logger.error(error_msg)
        return PingResult(
            latency=-1,
            success=False,
            error=error_msg
        )
