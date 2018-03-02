# -*- coding: utf-8 -*-
"""
A collection of useful file system utilities
"""

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import os
import time


def get_file_age(filename):
    """
    Returns age of file in seconds

    :param str filename: file to inspect

    .. versionadded:: 1.0.0
    """

    mtime = os.path.getmtime(filename)
    now = time.time()
    return int(now - mtime)


def touch(filename, create_dirs=False, timestamp=None):
    """
    Opens and closes *filename*, similarly to :program:`touch(1)`.
    If *filename* is a nested path and *create_dirs* is true, all
    intermediate directories will be created.

    :param str filename: path to the file to touch
    :param bool create_dirs: create all parent directories if necessary
    :param int timestamp: UNIX timestamp for *mtime* and *atime*

    .. versionadded:: 1.0.0
    """

    if create_dirs:
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
    open(filename, 'w').close()

    if timestamp:
        # Set atime and mtime to timestamp
        os.utime(filename, (timestamp, timestamp))
