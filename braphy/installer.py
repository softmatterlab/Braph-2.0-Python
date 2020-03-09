import PyInstaller.__main__
import os

ui_path = os.path.join(os.path.abspath("."), "gui/ui_files/*.ui")

PyInstaller.__main__.run([
    '--name=BraphyGui',
    '--onefile',
    '--windowed',
    '--hidden-import=pkg_resources.py2_warn',
    '--hidden-import=gui/icons_rc.py',
    '--add-data={}:braphy/gui/ui_files'.format(ui_path),
    os.path.join('gui','__main__.py'),
    ])
