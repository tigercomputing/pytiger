#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

from setuptools import setup, find_packages

setup(name='pytiger',
      version='1.2.0',
      description='Tiger Computing Ltd Python Utilities',
      author='Tiger Computing Ltd',
      author_email='info@tiger-computing.co.uk',
      package_dir = {'': 'src'},
      packages=find_packages('src'),
      install_requires=[
        'six',
      ]
)

