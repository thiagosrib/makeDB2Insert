from distutils.core import setup
import py2exe
#setup(console=['Gera Insert.py']) 

setup(
    options = {'py2exe': {'bundle_files': 3, 'compressed': True}},
    windows = [{'script': "Gera Insert.py"}],
    zipfile = None,
)