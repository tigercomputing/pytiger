# -*- coding: utf-8 -*-
"""
A simple plugin loading mechanism
"""

# Copyright © 2015-2023 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

# Idea originally borrowed and adapted from:
# https://copyninja.info/blog/dynamic-module-loading.html
# http://stackoverflow.com/a/3381582


import os

try:
    from .plugins_importlib import _Plugin
except ImportError:
    from .plugins_imp import _Plugin


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
        if dirent.startswith("__"):
            continue

        full_path = os.path.join(plugin_dir, dirent)

        # Load .py files as plugins
        if dirent.endswith(".py"):
            plugin_name = package + "." + os.path.splitext(dirent)[0]
            plugins.append(_Plugin(plugin_name, full_path, plugin_dir))
            continue

        # Load directories containing __init__.py
        if os.path.isdir(full_path):
            plugin_name = package + "." + dirent
            plugin_path = os.path.join(full_path, "__init__.py")
            if os.path.isfile(plugin_path):
                plugins.append(_Plugin(plugin_name, plugin_path, plugin_dir))

    # Now load the plugin modules
    modules = []
    for plugin in plugins:
        modules.append(plugin.load())

    return modules
