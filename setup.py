from setuptools import setup, find_packages

setup(name='MandeepPAD',
      version='0.0.6',
      author='Mandeep Bhutani',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['arrow'],
      entry_points='''
        [console_scripts]
        MandeepPAD=editor.mpad:main
        ''',
      )
