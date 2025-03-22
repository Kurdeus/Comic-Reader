# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['setup.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/styles.css', 'assets'), ('assets/scripts.js', 'assets'), ('assets/menu.svg', 'assets'), ('assets/menu-light.svg', 'assets'), ('assets/scroll.svg', 'assets'), ('assets/scroll-light.svg', 'assets'), ('assets/boot.template.html', 'assets'), ('assets/doc.template.html', 'assets'), ('assets/img.template.html', 'assets'), ('assets/roboto-regular.woff2', 'assets'), ('assets/roboto-bold.woff2', 'assets'), ('assets/zenscroll.js', 'assets')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='Comic Reader',
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
    icon='assets/app.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Comic Reader',
)
app = BUNDLE(
    coll,
    name='Comic Reader.app',
    icon='assets/app.ico',
    bundle_identifier=None,
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Images',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': [
                    'public.jpeg',
                    'public.png',
                    'com.compuserve.gif',
                    'org.webmproject.webp',
                    'com.microsoft.bmp',
                    'public.svg-image'
                ],
                'LSHandlerRank': 'Default',
                'NSExportableTypes': [
                    'public.jpeg',
                    'public.png',
                    'com.compuserve.gif',
                    'org.webmproject.webp',
                    'com.microsoft.bmp',
                    'public.svg-image'
                ]
            },
            {
                'CFBundleTypeName': 'Comic book archives',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': [
                    'public.comic.archive',
                    'public.zip-archive',
                    'org.7-zip.7-zip-archive',
                ],
                'NSExportableTypes': [
                    'public.comic.archive',
                    'public.zip-archive',
                    'org.7-zip.7-zip-archive',
                ]
            }
        ],
        'UTImportedTypeDeclarations': [
            {
                'UTTypeIdentifier': 'public.comic.archive',
                'UTTypeDescription': 'Comic book archive',
                'UTTypeConformsTo': ['public.data'],
                'UTTypeTagSpecification': {
                    'public.filename-extension': ['cbz', 'cb7']
                }
            }
        ]
    }
)
