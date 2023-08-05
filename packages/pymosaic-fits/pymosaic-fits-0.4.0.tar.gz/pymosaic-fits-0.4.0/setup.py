from setuptools import setup
import ast
import sys

setup_requires = ['setuptools >= 30.4.0', 'setuptools-git-version']

if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')


setup(description="pymosaic-fits",
      long_description=open('README.md').read(),
      version='0.4.0',
      include_package_data=True,
      setup_requires=setup_requires)
