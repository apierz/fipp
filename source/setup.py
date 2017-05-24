import sys
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'includes': [
            'fipp',
            'account',
            'cv_con'
        ],
        'path': sys.path + ['fipp']
    }
}

executables = [
    Executable('fipp.py'),
 ]

setup(name='fipp',
      version='0.1.1',
      description='Feed Interface Poorly written in Python',
      options=options,
      executables=executables
      )
