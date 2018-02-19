# -*- coding: utf-8 -*-

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

from __future__ import absolute_import

import logging
import logging.config
import os.path
import sys
import syslog
import textwrap
import unittest
from six import StringIO

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from .syslog import (
    PRIORITY_NAMES, FACILITY_NAMES, priority, facility, encode_priority,
    _map_priority, SyslogHandler)


class TestSyslogSupport(unittest.TestCase):
    def test_priority_int(self):
        for name, value in PRIORITY_NAMES.items():
            self.assertEqual(value, priority(value))

    def test_priority_str(self):
        for name, value in PRIORITY_NAMES.items():
            self.assertEqual(value, priority(name))

    def test_priority_str_invalid(self):
        self.assertRaises(ValueError, priority, 'foobar')

    def test_priority_invalid(self):
        self.assertRaises(TypeError, priority, object())

    ####################
    def test_facility_int(self):
        for name, value in FACILITY_NAMES.items():
            self.assertEqual(value, facility(value))

    def test_facility_str(self):
        for name, value in FACILITY_NAMES.items():
            self.assertEqual(value, facility(name))

    def test_facility_str_invalid(self):
        self.assertRaises(ValueError, facility, 'foobar')

    def test_facility_invalid(self):
        self.assertRaises(TypeError, facility, object())

    ####################
    def test_encode_priority(self):
        SAMPLE_ENCODINGS = [
            ('user', 'crit',     (1 << 3) | 2),
            ('auth', 'emerg',    (4 << 3) | 0),
            ('mail', 'debug',    (2 << 3) | 7),
            ('cron', 'warning',  (9 << 3) | 4),
            ('kern', 'emerg',    (0 << 3) | 0),
            ('local7', 'debug', (23 << 3) | 7),
        ]
        for fac, pri, expect in SAMPLE_ENCODINGS:
            value = encode_priority(fac, pri)
            self.assertEqual(value, expect,
                             "%d != %s:%s (%d)" % (value, fac, pri, expect))

    ####################
    def test_map_priority(self):
        SAMPLE_MAPPINGS = [
            (logging.CRITICAL, syslog.LOG_CRIT),
            (logging.ERROR, syslog.LOG_ERR),
            (logging.WARNING, syslog.LOG_WARNING),
            (logging.INFO, syslog.LOG_INFO),
            (logging.DEBUG, syslog.LOG_DEBUG),
            (100, syslog.LOG_CRIT),     # x > CRITICAL
            (45, syslog.LOG_CRIT),      # CRITICAL > x > ERROR
            (35, syslog.LOG_ERR),       # ERROR > x > WARNING
            (25, syslog.LOG_WARNING),   # WARNING > x > INFO
            (15, syslog.LOG_INFO),      # INFO > x > DEBUG
            (5, syslog.LOG_DEBUG),      # DEBUG > x
        ]
        for lvl, prio in SAMPLE_MAPPINGS:
            value = _map_priority(lvl)
            self.assertEqual(prio, value,
                             "%d => %d; expected %d" % (lvl, value, prio))


class TestSyslogFormatter(unittest.TestCase):
    config = """
    [loggers]
    keys=root

    [handlers]
    keys=hand1

    [formatters]
    keys=form1

    [logger_root]
    level=NOTSET
    handlers=hand1

    [handler_hand1]
    class=StreamHandler
    level=NOTSET
    formatter=form1
    args=(sys.stdout,)

    [formatter_form1]
    class=pytiger.logging.syslog.SyslogFormatter
    format=%(levelname)s:%(name)s:%(message)s
    datefmt=
    """

    def test_formatter_exception(self):
        with patch('sys.stdout', new=StringIO()) as out:
            logging.config.fileConfig(StringIO(textwrap.dedent(self.config)))
            try:
                raise RuntimeError()
            except RuntimeError:
                logging.exception("just testing")
            sys.stdout.seek(0)
            self.assertEqual(out.getvalue(),
                             "ERROR:root:just testing\n")


class TestSyslogHandler(unittest.TestCase):
    config1 = """
    [loggers]
    keys=root

    [handlers]
    keys=hand1

    [formatters]
    keys=form1

    [logger_root]
    level=NOTSET
    handlers=hand1

    [handler_hand1]
    class=pytiger.logging.syslog.SyslogHandler
    level=NOTSET
    formatter=form1
    args=()

    [formatter_form1]
    class=pytiger.logging.syslog.SyslogFormatter
    format=%(levelname)s:%(name)s:%(message)s
    datefmt=
    """

    config2 = """
    [loggers]
    keys=root

    [handlers]
    keys=hand1

    [formatters]
    keys=

    [logger_root]
    level=NOTSET
    handlers=hand1

    [handler_hand1]
    class=pytiger.logging.syslog.SyslogHandler
    level=NOTSET
    args=("config2",)
    """

    def apply_config(self, conf):
        logging.config.fileConfig(StringIO(textwrap.dedent(conf)))

    def test_openlog_default(self):
        # In Python 2.6 ident must be a string so we need to do what
        # SyslogHandler.__init__() does to get an ident string.
        ident = os.path.basename(sys.argv[0])

        with patch('syslog.openlog') as openlog:
            self.apply_config(self.config1)
            openlog.assert_called_once_with(
                ident, syslog.LOG_PID, syslog.LOG_USER)

    def test_openlog_ident(self):
        with patch('syslog.openlog') as openlog:
            self.apply_config(self.config2)
            openlog.assert_called_once_with(
                'config2', syslog.LOG_PID, syslog.LOG_USER)

    def test_logging(self):
        self.apply_config(self.config1)
        logger = logging.getLogger()
        handler = logger.handlers[0]

        with patch('syslog.syslog') as _syslog:
            logger.critical('something critical')
            _syslog.assert_called_once_with(
                syslog.LOG_USER | syslog.LOG_CRIT,
                "CRITICAL:root:something critical")

        with patch('syslog.syslog') as _syslog:
            logger.warning('something you should know')
            _syslog.assert_called_once_with(
                syslog.LOG_USER | syslog.LOG_WARNING,
                "WARNING:root:something you should know")

        with patch('syslog.syslog') as _syslog:
            logger.debug('the authors may want to know...')
            _syslog.assert_called_once_with(
                syslog.LOG_USER | syslog.LOG_DEBUG,
                "DEBUG:root:the authors may want to know...")

        self.assertTrue(isinstance(handler, SyslogHandler))
        handler.facility = 'uucp'

        with patch('syslog.syslog') as _syslog:
            logger.info('something happened')
            _syslog.assert_called_once_with(
                syslog.LOG_UUCP | syslog.LOG_INFO,
                "INFO:root:something happened")
