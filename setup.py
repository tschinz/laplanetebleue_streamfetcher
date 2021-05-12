from setuptools import find_packages, setup
from pathlib import Path
import src


def glob_fix(package_name, glob):
  # this assumes setup.py lives in the folder that contains the package
  package_path = Path(f'./{package_name}').resolve()
  return [str(path.relative_to(package_path))
          for path in package_path.glob(glob)]


setup(
  name='src',
  packages=find_packages(),
  version=src.__version__,
  python_requires='>=3.8',
  description='La Planète Bleue Streamfetcher',
  author='tschinz',
  license='MIT',

  package_data={
    'src': [
      *glob_fix('src/', 'assets/**/*'),
    ]
  },

  install_requires=[
    'beautifulsoup4',
    'certifi',
    'lxml',
    'mutagen',
    'pycurl',
    'soupsieve',
    'wincertstore'
  ],

)
