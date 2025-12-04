# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-04

### Added
- Complete project restructure with modular architecture
- New `checkpcspecs.core` module for hardware checking
- New `checkpcspecs.network` module for network testing
- New `checkpcspecs.ui` module for GUI components
- New `checkpcspecs.utils` module for utilities
- Type hints throughout the codebase
- Comprehensive docstrings
- Better error handling and logging
- Fallback methods for network tests
- Proper async/await support
- Package installation support (`pip install -e .`)
- CLI entry point (`checkpcspecs` command)
- Development dependencies and tooling

### Changed
- Refactored monolithic `windowed.py` into modular structure
- Improved UI component reusability
- Enhanced network testing reliability
- Better resource management
- Updated PyInstaller spec file
- Modernized README with full documentation

### Improved
- Code organization and maintainability
- Error messages and user feedback
- Performance and reliability
- Documentation quality

### Removed
- Deprecated `internal/` modules (migrated to package structure)
- Old monolithic architecture

## [1.0.0] - 2022-08-16

### Added
- Initial release
- Basic PC specs checking
- Windows OS detection
- CPU and RAM checking
- Disk type detection
- Network speed test
- Ping test
- Tkinter GUI
- PyInstaller support
