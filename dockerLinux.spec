# -*- mode: python ; coding: utf-8 -*-
#pyinstaller dockerLinux.spec MUST BE RUN ON LINUX NOT WINDOWS
from PyInstaller.utils.hooks import collect_submodules
import jpype

a = Analysis(
    ['Main/main.py'],
    pathex=[],
    binaries=[],
    datas=[('Main/CentralFramework', 'CentralFramework'), 
            ('Main/FrontEnd', 'FrontEnd'),
            ('Main/GameHandler', 'GameHandler'), 
            ('Main/Plugins', 'Plugins'), 
            ('Main/ProjectHandler', 'ProjectHandler'),
            ('Main', 'Main'),
            (jpype.__path__[0], "jpype")],
    hiddenimports=[
    'PyQt5',
    'PyQt5.sip',
    'PyQt5.QtWidgets',
    'PyQt5.Qsci',
    'PyQt5.QtGui',
    'PyQt5.QtCore',
    'sys',
    'os',
    'glob',
    'queue',
    'threading',
    're',
    'pathlib',
    'importlib.util',
    'abc',
    'tkinter',
    'tkinter.tix',
    'click',
    'jpype',
    'jdk'
] + collect_submodules('jpype'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='mainLinux',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
