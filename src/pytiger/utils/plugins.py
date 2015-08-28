# -*- coding: utf-8 -*-
"""
A simple plugin loading mechanism
"""

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

# Idea borrowed and adapted from:
# https://copyninja.info/blog/dynamic-module-loading.html
# http://stackoverflow.com/a/3381582

import imp
import os


def load(plugin_dir, package=__name__):
    """
    Load Python modules and packages from a directory.

    This function will list the contents of ``plugin_dir`` and load any Python
    modules (files ending ``.py``) or packages (directories with a
    ``__init__.py`` file) found within it. Sub-directories are not searched.
    Modules are compiled as they are loaded, if necessary.

    Plugins are loaded within a package name as supplied to this function in
    the optional ``package`` parameter. If this is not provided, this defaults
    to ``pytiger.utils.plugins``. The module name supplied in ``package`` must
    already be known to Python (i.e. in ``sys.modules``).

    The function returns a list of python module objects, one per loaded module
    or package.

    :param str plugin_dir: The path to the directory to load plugins from.
    :param str package: Python package to load the plugins into.

    .. versionadded:: 1.1.0
    """
    plugin_dir = os.path.realpath(plugin_dir)

    # Discover the list of plugins
    plugins = []
    for dirent in os.listdir(plugin_dir):
        # skip __init__.py
        if dirent.startswith('__'):
            continue

        # Load .py files as plugins
        if dirent.endswith('.py'):
            plugins.append(os.path.splitext(dirent)[0])
            continue

        # Load directories containing __init__.py
        full_path = os.path.join(plugin_dir, dirent)
        if os.path.isdir(full_path):
            if os.path.isfile(os.path.join(full_path, '__init__.py')):
                plugins.append(dirent)

    # Now load the plugin modules
    modules = []
    for plugin in plugins:
        f, path, desc = imp.find_module(plugin, [plugin_dir])
        module = imp.load_module(package + '.' + plugin, f, path, desc)
        modules.append(module)

    return modules
