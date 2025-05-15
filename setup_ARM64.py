# setup.py
from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
    'includes': [
        'pygame', 'pygame.mixer', 'pygame.font',
        'jaraco.text'
    ],
    'excludes': [
        'PyInstaller', 'django',
        'PyInstaller.hooks', 'django.core.cache'
    ],
    'resources': ['images', 'sounds'],
    'iconfile': 'appicon.icns',       # ← 指定你的 .icns 文件
    'plist': {
        'CFBundleName': 'Whats',
        'CFBundleShortVersionString': '1.0',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
