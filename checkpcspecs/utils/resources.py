"""Resource path management for PyInstaller compatibility."""

import os
import sys
from pathlib import Path
from typing import Optional


class ResourceManager:
    """Manages resource paths for bundled applications."""

    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        """Get absolute path to resource, works for dev and PyInstaller.
        
        Args:
            relative_path: Relative path to resource
            
        Returns:
            Absolute path to resource
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            base_path = Path.cwd()

        return base_path / relative_path

    @staticmethod
    def get_icon_path() -> Optional[Path]:
        """Get path to application icon."""
        icon_path = ResourceManager.get_resource_path('icon.ico')
        return icon_path if icon_path.exists() else None

    @staticmethod
    def get_logo_path() -> Optional[Path]:
        """Get path to application logo."""
        logo_path = ResourceManager.get_resource_path('logo.png')
        return logo_path if logo_path.exists() else None
