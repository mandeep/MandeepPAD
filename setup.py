from setuptools import setup

setup(name='MandeepPAD',
      version='0.9',
      author='Mandeep Bhutani',
      packages=['mpad', 'mpad.images'],
      package_data={'mpad.images': '*.png'},
      install_requires=['arrow'],
      entry_points='''
        [console_scripts]
        MandeepPAD=mpad.editor:main
        ''',
      )
