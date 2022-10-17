# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/DELL/PycharmProjects/CheckPCSpecs/windowed.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/DELL/PycharmProjects/CheckPCSpecs/logo.png', '.'), ('C:/Users/DELL/PycharmProjects/CheckPCSpecs/icon.ico', '.')],
    hiddenimports=['speedtest', 'cpuinfo', 'psutil'],
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
    name='windowed',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['C:\\Users\\DELL\\PycharmProjects\\CheckPCSpecs\\icon.ico'],
)
