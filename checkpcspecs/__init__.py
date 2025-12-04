"""CheckPCSpecs - PC Specifications Checker.

A tool to verify if a PC meets minimum system requirements.
"""

__version__ = '2.0.0'
__author__ = 'apeks827'

from .app import Application
from .core import (
    OSResult,
    ArchResult,
    RAMResult,
    CPUResult,
    DiskResult,
    SpecsChecker
)
from .network import (
    SpeedTester,
    PingTester,
    NetworkEvaluator
)
from .utils import (
    ResourceManager,
    ScoreCalculator,
    PCScore,
    PCVerdict
)

__all__ = [
    'Application',
    'OSResult',
    'ArchResult',
    'RAMResult',
    'CPUResult',
    'DiskResult',
    'SpecsChecker',
    'SpeedTester',
    'PingTester',
    'NetworkEvaluator',
    'ResourceManager',
    'ScoreCalculator',
    'PCScore',
    'PCVerdict',
]
