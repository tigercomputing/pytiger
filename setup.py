#!/usr/bin/python

from setuptools import setup, find_packages

setup(name='pytiger',
      version='1.0.0~alpha1',
      description='Tiger Computing Ltd Python Utilities',
      author='Tiger Computing Ltd',
      author_email='info@tiger-computing.co.uk',
      package_dir = {'': 'src'},
      packages=find_packages('src'),
)

