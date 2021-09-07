# -*- mode: python ; coding: utf-8 -*-


#  pyi-makespec -F -w main.py
#  pyinstaller -F main.spec


block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/bo/my/git/python_notes/image_convert'],
             binaries=[],
             datas=[('res','res')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
app = BUNDLE(exe,
             name='main.app',
             icon=None,
             bundle_identifier=None)
