#!/usr/bin/env python

from setuptools import setup

setup(name='SoundCloudChallenge',
      description='Python Distribution Utilities',
      author='Farshad Fahimi',
      version='0.0.1',

      packages=['src',
                'src.configuration',
                'src.data_handling',
                'src.search_ranking',
                'src.tests'],
      requires='pandas',
)
