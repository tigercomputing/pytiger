# -*- coding: utf-8 -*-

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import warnings
from pytiger.monitoring.monitoringcheck import MonitoringCheck

warnings.warn('NagiosCheck is deprecated, use MonitoringCheck() instead',
              DeprecationWarning)

NagiosCheck = MonitoringCheck
