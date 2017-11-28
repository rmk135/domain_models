"""`Domain models` setup script."""

import os
import re

from setuptools import setup
from setuptools import Command


# Getting description:
with open('README.rst') as readme_file:
    description = readme_file.read()

# Getting requirements:
with open('requirements.txt') as version:
    requirements = version.readlines()

# Getting version:
with open('domain_models/__init__.py') as init_file:
    version = re.search('VERSION = \'(.*?)\'', init_file.read()).group(1)


class PublishCommand(Command):
    """Setuptools `publish` command."""

    description = "Publish current distribution to PyPi and create tag"
    user_options = []

    def initialize_options(self):
        """Init options."""

    def finalize_options(self):
        """Finalize options."""

    def run(self):
        """Command execution."""
        self.run_command('sdist')
        self.run_command('upload')
        os.system('git tag -a {0} -m \'version {0}\''.format(version))
        os.system('git push --tags')


setup(name='domain-models',
      version=version,
      description='Domain models framework for Python projects',
      long_description=description,
      author='ETS Labs',
      author_email='rmogilatov@gmail.com',
      maintainer='ETS Labs',
      maintainer_email='rmogilatov@gmail.com',
      url='https://github.com/ets-labs/python-domain-models',
      bugtrack_url='https://github.com/ets-labs/python-domain-models/issues',
      download_url='https://pypi.python.org/pypi/domain_models',
      license='BSD New',
      packages=['domain_models'],
      platforms=['any'],
      zip_safe=True,
      install_requires=requirements,
      cmdclass={
          'publish': PublishCommand,
      },
      keywords=[
          'Domain models',
          'Domain modelling',
          'Domain driven design',
          'Domain driven development',
          'DDD',
          'Models',
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
