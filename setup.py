import sys

from setuptools import setup


if sys.version_info.major == 3 and sys.version_info.minor > 5:
    requirements = ['pyqt5']
else:
    requirements = []


setup(name='MandeepPAD',
      version='0.16.0',
      author='Mandeep',
      packages=['mpad', 'mpad.images'],
      package_data={'mpad.images': ['*.png']},
      install_requires=requirements,
      entry_points='''
        [console_scripts]
        MandeepPAD=mpad.editor:main
        '''
      )
