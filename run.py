#!/usr/bin/env python
"""Standalone entry point for CheckPCSpecs.

This allows running the application without installing it as a package.

Usage:
    python run.py
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == '__main__':
    from checkpcspecs.app import main
    main()
