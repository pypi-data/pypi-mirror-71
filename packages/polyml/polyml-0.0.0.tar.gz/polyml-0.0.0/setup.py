#!/usr/bin/env python

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='polyml',
      version='0.0.0',
      description='Polyaxon model management.',
      maintainer="Polyaxon, Inc.",
      maintainer_email="contact@polyaxon.com",
      author="Polyaxon, Inc.",
      author_email="contact@polyaxon.com",
      url="https://github.com/polyaxon/polyaxon",
      license="Apache 2.0",
      platforms="any",
      packages=find_packages(),
      keywords=[
          'polyaxon',
          'polyset',
          'deep-learning',
          'machine-learning',
          'workflow',
          'events',
          'hooks',
          'kubernetes',
      ],
      install_requires=[],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      tests_require=[],
      cmdclass={'test': PyTest})
