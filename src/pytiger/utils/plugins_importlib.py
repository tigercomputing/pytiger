# -*- coding: utf-8 -*-
"""
A plugin loader using importlib.util (Python 3.5+)
"""

# Copyright © 2023 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import sys
from importlib.util import spec_from_file_location, module_from_spec


class _Plugin:
    def __init__(self, module_name, file_path, plugin_dir):
        self.module_name = module_name
        self.file_path = file_path
        self.plugin_dir = plugin_dir

    def load(self):
        spec = spec_from_file_location(
            self.module_name,
            self.file_path,
        )

        module = module_from_spec(spec)
        sys.modules[self.module_name] = module
        spec.loader.exec_module(module)

        return module
