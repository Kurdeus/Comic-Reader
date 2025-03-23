# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['setup.py'],
    pathex=[],
    binaries=[],
    datas=[('assets\\styles.css', 'assets'), ('assets\\scripts.js', 'assets'), ('assets\\menu.svg', 'assets'), ('assets\\menu-light.svg', 'assets'), ('assets\\scroll.svg', 'assets'), ('assets\\scroll-light.svg', 'assets'), ('assets\\boot.template.html', 'assets'), ('assets\\doc.template.html', 'assets'), ('assets\\img.template.html', 'assets'), ('assets\\roboto-regular.woff2', 'assets'), ('assets\\roboto-bold.woff2', 'assets'), ('assets\\zenscroll.js', 'assets'), ('version', '.'), ('unrar.exe', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ComicReader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\app.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ComicReader',
)
