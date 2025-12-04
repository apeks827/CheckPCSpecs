"""Network testing module for CheckPCSpecs."""

from .speedtest import SpeedTester, SpeedTestResult
from .ping import PingTester, PingResult

__all__ = ['SpeedTester', 'SpeedTestResult', 'PingTester', 'PingResult']
