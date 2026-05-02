# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

if sys.platform == 'win32':
  icon_file = os.path.join('icon', 'favicon.ico')
elif sys.platform == 'darwin':
  icon_file = os.path.join('icon', 'favicon.icns')
else:
  icon_file = os.path.join('icon', 'favicon.png')

a = Analysis(
  ['main.py'],
  pathex=[],
  binaries=[],
  datas=[('icon', 'icon'), ('template', 'template')],
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
  name='Pyder',
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
  entitlements_file=None,
  icon=icon_file,
)
