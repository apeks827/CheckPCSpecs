"""Custom exceptions for CheckPCSpecs."""


class CheckPCSpecsError(Exception):
    """Base exception for CheckPCSpecs."""
    pass


class SystemCheckError(CheckPCSpecsError):
    """Error during system check."""
    pass


class NetworkTestError(CheckPCSpecsError):
    """Error during network test."""
    pass


class SpeedTestError(NetworkTestError):
    """Error during speed test."""
    pass


class PingTestError(NetworkTestError):
    """Error during ping test."""
    pass


class HardwareDetectionError(SystemCheckError):
    """Error detecting hardware."""
    pass


class ConfigurationError(CheckPCSpecsError):
    """Configuration error."""
    pass
