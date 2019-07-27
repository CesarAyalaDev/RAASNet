# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['RAASNet.py'],
             pathex=['C:\\Users\\leon\\Desktop\\python\\RAASNet'],
             binaries=[],
             datas=[('images/logo2.png', 'images')],
             hiddenimports=['tkinter', 'tkinter.ttk', 'ttkthemes', 'pymsgbox'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='RAASNet',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='images\\icon.ico')
