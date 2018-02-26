# -*- coding: utf-8 -*-
# Copyright © 2018  Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details
"""
.. versionadded:: 1.2.0

Configure the Python :mod:`logging` system following Tiger conventions.

This module, combined with the Python :mod:`logging` package, is the
spiritual successor to the deprecated :mod:`pytiger.logging.legacy` module.

Example usage:

>>> pytiger.logging.config.basic_config()
>>> log = logging.getLogger(__name__)
>>> log.warning('Unable to biggle')
W: Unable to biggle
>>> log.error('Abandon ship, all ye who run this')
E: Abandon ship, all ye who run this
"""

from __future__ import absolute_import

import logging

from .syslog import SyslogFormatter, SyslogHandler


#: Log format string following Tiger Computing conventions.
TCL_FORMAT = "%(leveltag)s: %(message)s"


class LevelTagFilter(object):
    """
    Log filter that adds the `leveltag` field.

    This :class:`logging.Filter` sub-class (using duck-typing) is used to add
    the `leveltag` field to :class:`logging.LogRecord` objects so that the tag
    is available for use when formatted with the :const:`TCL_FORMAT` format
    string.
    """
    def filter(self, record):
        # Extract the first character of the level name
        record.leveltag = record.levelname[0]

        # We never actually filter messages out, just abuse filtering to add an
        # extra field to the LogRecord
        return True


def basic_config(fmt=None, datefmt=None, level=None, stderr=True,
                 stderr_level=None, syslog=True, syslog_level=None):
    """
    Perform basic configuration of the Python :mod:`logging` system.

    This is very similar to :func:`logging.basicConfig` but designed to follow
    Tiger Computing's logging conventions: messages are logged to stderr and to
    syslog, and messages are prefixed with a single character tag describing
    the log level.

    This function does nothing if the root logger already has handlers
    configured, therefore this function will only configure logging once. It is
    a convenience method to do one-shot configuration of the Python logging
    package.

    The default behaviour is to:

    * Create a :class:`logging.StreamHandler` which writes to
      :data:`sys.stderr`.
    * Create a :class:`pytiger.logging.syslog.SyslogHandler`, which forwards
      messages to syslog using :func:`syslog.syslog`.
    * Add the :class:`LevelTagFilter` to the above handlers.
    * Set a formatter on the above handlers using the :const:`TCL_FORMAT`
      format string.
    * Add the handlers to the root logger.
    * Sets the root logger's log level to :const:`logging.INFO`.

    :param str fmt: Use the specified format string for the handlers.
    :param str datefmt: Use the specified date/time format.
    :param level: Set the root logger's log level.
    :param bool stderr: Determine whether the stderr `StreamHandler` is
                        configured or added to the root logger.
    :param stderr_level: Set the stderr logger's log level.
    :param bool syslog: Determine whether the `SyslogHandler` is
                        configured or added to the root logger.
    :param syslog_level: Set the syslog logger's log level.
    """
    root = logging.getLogger()

    logging._acquireLock()
    try:
        # Do nothing if the root logger already has handlers configured
        if len(root.handlers) == 0:
            ltf = LevelTagFilter()

            if fmt is None:
                fmt = TCL_FORMAT

            # Configure output to stderr if desired
            if stderr:
                h = logging.StreamHandler()
                h.setFormatter(logging.Formatter(fmt, datefmt))
                h.addFilter(ltf)

                if stderr_level is not None:
                    h.setLevel(stderr_level)

                root.addHandler(h)

            # Configure output to syslog if desired
            if syslog:
                h = SyslogHandler()
                h.setFormatter(SyslogFormatter(fmt, datefmt))
                h.addFilter(ltf)

                if syslog_level is not None:
                    h.setLevel(syslog_level)

                root.addHandler(h)

            # Set the standard log level threshold for the root logger
            if level is None:
                level = logging.INFO
            root.setLevel(level)
    finally:
        logging._releaseLock()
