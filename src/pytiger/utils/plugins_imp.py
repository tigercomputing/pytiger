# -*- coding: utf-8 -*-
"""
A plugin loader using imp (Python <3.4)
"""

# Copyright © 2015-2023 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import imp


class _Plugin:
    def __init__(self, module_name, file_path, plugin_dir):
        self.module_name = module_name
        self.file_path = file_path
        self.plugin_dir = plugin_dir

    def load(self):
        plugin = self.module_name.split(".")[-1]

        f, path, desc = imp.find_module(plugin, [self.plugin_dir])
        module = imp.load_module(self.module_name, f, path, desc)

        return module
