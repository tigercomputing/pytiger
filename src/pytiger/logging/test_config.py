# -*- coding: utf-8 -*-

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

from __future__ import absolute_import


import logging
import syslog
import unittest
from six import StringIO

try:
    from unittest.mock import call, patch
except ImportError:
    from mock import call, patch

from .config import LevelTagFilter, basic_config


class TestLevelTagFilter(unittest.TestCase):
    def test_level_tag_filter(self):
        out = StringIO()
        h = logging.StreamHandler(out)
        h.setFormatter(logging.Formatter(
            '%(levelname)s:%(leveltag)s:%(name)s:%(message)s'))
        h.addFilter(LevelTagFilter())
        logging.getLogger().addHandler(h)
        logging.warning('Could not frob; continuing')
        out.seek(0)
        self.assertEqual(out.getvalue(),
                         'WARNING:W:root:Could not frob; continuing\n')


class TestBasicConfig(unittest.TestCase):
    def setUp(self):
        # Clear the root logger's handlers otherwise basic_config() refuses to
        # do anything. Test frameworks like Nose set up their own loggers so we
        # have to work around that.
        self.handlers = logging.root.handlers
        logging.root.handlers = []

    def tearDown(self):
        for h in logging.root.handlers[:]:
            if h not in self.handlers:
                logging.root.removeHandler(h)

        logging.root.handlers = self.handlers

        super(TestBasicConfig, self).tearDown()

    def _basic_config(self, **kwargs):
        basic_config(**kwargs)

        # Put the test framework's logging handlers back on the root handler so
        # that we can get useful debugging information should the tests fail.
        logging.root.handlers.extend(self.handlers)

    @patch('sys.stderr', new_callable=StringIO)
    @patch('syslog.syslog')
    def test_defaults(self, syslog_, stderr):
        self._basic_config()

        logging.warning('Unable to biggle')
        logging.info('Could not frob; continuing')
        logging.debug('Piffle!')

        self.assertEqual(
            stderr.getvalue(),
            'W: Unable to biggle\nI: Could not frob; continuing\n')
        calls = [
            call(syslog.LOG_USER | syslog.LOG_WARNING,
                 'W: Unable to biggle'),
            call(syslog.LOG_USER | syslog.LOG_INFO,
                 'I: Could not frob; continuing'),
        ]
        syslog_.assert_has_calls(calls)
        self.assertEqual(syslog_.call_count, len(calls))

    def test_already_configured(self):
        h = logging.StreamHandler()
        logging.root.addHandler(h)

        self.assertEqual(logging.root.handlers, [h])

        # Don't use self._basic_config() to avoid putting logging framework's
        # handlers back on the root logger.
        basic_config()

        self.assertEqual(logging.root.handlers, [h])
        self.assertTrue(logging.root.handlers[0] is h)

    @patch('sys.stderr', new_callable=StringIO)
    @patch('syslog.syslog')
    def test_format(self, syslog_, stderr):
        self._basic_config(fmt='%(leveltag)s:%(name)s:%(message)s')

        logging.warning('Unable to biggle')

        self.assertEqual(stderr.getvalue(), 'W:root:Unable to biggle\n')
        syslog_.assert_called_once_with(
            syslog.LOG_USER | syslog.LOG_WARNING,
            'W:root:Unable to biggle')

    @patch('sys.stderr', new_callable=StringIO)
    @patch('syslog.syslog')
    def test_stderr_disabled(self, syslog_, stderr):
        self._basic_config(stderr=False)

        logging.warning('Unable to biggle')

        self.assertEqual(stderr.getvalue(), '')
        syslog_.assert_called_once_with(
            syslog.LOG_USER | syslog.LOG_WARNING,
            'W: Unable to biggle')

    @patch('sys.stderr', new_callable=StringIO)
    @patch('syslog.syslog')
    def test_syslog_disabled(self, syslog_, stderr):
        self._basic_config(syslog=False)

        logging.warning('Unable to biggle')

        self.assertEqual(stderr.getvalue(), 'W: Unable to biggle\n')
        syslog_.assert_not_called()

    @patch('sys.stderr', new_callable=StringIO)
    @patch('syslog.syslog')
    def test_stderr_level(self, syslog_, stderr):
        self._basic_config(stderr_level=logging.WARNING)

        logging.warning('Unable to biggle')
        logging.info('Could not frob; continuing')

        self.assertEqual(stderr.getvalue(), 'W: Unable to biggle\n')
        calls = [
            call(syslog.LOG_USER | syslog.LOG_WARNING,
                 'W: Unable to biggle'),
            call(syslog.LOG_USER | syslog.LOG_INFO,
                 'I: Could not frob; continuing'),
        ]
        syslog_.assert_has_calls(calls)
        self.assertEqual(syslog_.call_count, len(calls))

    @patch('sys.stderr', new_callable=StringIO)
    @patch('syslog.syslog')
    def test_syslog_level(self, syslog_, stderr):
        self._basic_config(syslog_level=logging.WARNING)

        logging.warning('Unable to biggle')
        logging.info('Could not frob; continuing')

        self.assertEqual(
            stderr.getvalue(),
            'W: Unable to biggle\nI: Could not frob; continuing\n')
        syslog_.assert_called_once_with(
            syslog.LOG_USER | syslog.LOG_WARNING,
            'W: Unable to biggle')

    @patch('sys.stderr', new_callable=StringIO)
    @patch('syslog.syslog')
    def test_level(self, syslog_, stderr):
        self._basic_config(level=logging.WARNING)

        logging.warning('Unable to biggle')
        logging.info('Could not frob; continuing')

        self.assertEqual(
            stderr.getvalue(),
            'W: Unable to biggle\n')
        syslog_.assert_called_once_with(
            syslog.LOG_USER | syslog.LOG_WARNING,
            'W: Unable to biggle')
