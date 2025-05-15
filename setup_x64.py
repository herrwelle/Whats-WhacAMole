from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': False,  # 必须关闭！Pygame不需要这个
    'packages': ['pygame'],
    'includes': ['pygame', 'pygame.mixer', 'pygame.font'],
    'excludes': ['PyInstaller', 'django'],
    'resources': ['images', 'sounds'],
    'iconfile': 'appicon.icns',
    'plist': {
        'CFBundleName': 'Whats',
        'CFBundleShortVersionString': '1.0.1',
        'CFBundleIdentifier': 'com.yourcompany.Whats',
        
        # 窗口行为关键配置
        'NSHighResolutionCapable': True,
        'LSUIElement': False,       # 必须False！显示Dock图标
        'LSBackgroundOnly': False,  # 必须False！禁止后台模式
        
        # 启动模式优化
        'NSRequiresAquaSystemAppearance': True,  # 强制使用亮色模式
        'NSSupportsAutomaticGraphicsSwitching': True,  # 显卡兼容
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
