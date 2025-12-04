# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for CheckPCSpecs."""

from PyInstaller.utils.hooks import collect_data_files
import os

block_cipher = None

# Collect all data files
datas = [
    ('icon.ico', '.'),
    ('logo.png', '.'),
]

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PIL._tkinter_finder',
    'pkg_resources.py2_warn',
    'nest_asyncio',
    'icmplib',
    'cpuinfo',
    'speedtest',
]

a = Analysis(
    ['checkpcspecs/__main__.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CheckPCSpecs',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
