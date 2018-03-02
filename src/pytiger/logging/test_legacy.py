# -*- coding: utf-8 -*-

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import unittest
from . import legacy
from mock import patch
from six import StringIO


class TestLegacySyslogger(unittest.TestCase):

    def setUp(self):
        self.logger = legacy.LegacySyslogger()

    ####################
    def test_default_members(self):
        required_attributes = ('_log_level', '_log_to_stdout',
                               '_log_to_syslog', '_syslog_name',)
        for attr in required_attributes:
            self.assertTrue(attr in self.logger.__dict__,
                            "Required attribute {attr} is missing"
                            .format(attr=attr))

    ####################
    def test_property_log_level(self):
        self.assertFalse(
            -9999 in legacy.LOGLEVELS,
            'This test needs checking: -9999 has become a valid log level')
        self.assertRaises(ValueError, setattr, self.logger, 'log_level', -9999)
        for level in legacy.LOGLEVELS:
            self.logger.log_level = level
            self.assertEqual(level, self.logger.log_level)

    def test_property_log_to_stdout(self):
        for v in (None, '', 'string'):
            self.assertRaises(ValueError, setattr, self.logger,
                              'log_to_stdout', v)
        for v in (True, False, True, False):
            self.logger.log_to_stdout = v
            self.assertEqual(v, self.logger.log_to_stdout)

    def test_property_log_to_syslog(self):
        for v in (None, '', 'string'):
            self.assertRaises(ValueError, setattr, self.logger,
                              'log_to_syslog', v)
        for v in (True, False, True, False):
            self.logger.log_to_syslog = v
            self.assertEqual(v, self.logger.log_to_syslog)

    def test_property_syslog_name(self):
        for v in (True, False, 1, None):
            self.assertRaises(ValueError, setattr, self.logger,
                              'syslog_name', v)
        self.logger.syslog_name = 'a_string'
        self.assertEqual(self.logger.syslog_name, 'a_string')

    ####################
    @patch('pytiger.logging.legacy.LegacySyslogger.log')
    def test_debug(self, mock_log):
        self.logger.debug('test string')
        mock_log.assert_called_once_with(legacy.DEBUG, 'test string')

    @patch('pytiger.logging.legacy.LegacySyslogger.log')
    def test_info(self, mock_log):
        self.logger.info('test string')
        mock_log.assert_called_once_with(legacy.INFO, 'test string')

    @patch('pytiger.logging.legacy.LegacySyslogger.log')
    def test_warning(self, mock_log):
        self.logger.warning('test string')
        mock_log.assert_called_once_with(legacy.WARNING, 'test string')

    @patch('pytiger.logging.legacy.LegacySyslogger.log')
    def test_error(self, mock_log):
        self.logger.error('test string')
        mock_log.assert_called_once_with(legacy.ERROR, 'test string')

    ####################
    def test_prefix_message(self):
        self.assertFalse(
            -9999 in legacy.LOGPREFIX,
            'This test needs checking: -9999 has become a valid log prefix '
            'index')
        self.assertEqual(self.logger._prefix_message(-9999, 'test'),
                         'test')
        for level, prefix in legacy.LOGPREFIX.items():
            self.assertEqual(self.logger._prefix_message(level, 'test'),
                             prefix + ': test')

    ####################
    @patch('syslog.syslog')
    def test_log_to_syslog(self, mock_syslog):
        # The default minimum log level is DEBUG with no tag,
        # so we'll assume that's the case
        # (that means we're also testing output with no tag, which
        # is ok for now)
        self.logger.log_to_stdout = False  # makes the test runner noisy
        self.logger.log(legacy.DEBUG, 'test message')
        mock_syslog.assert_called_once_with('D: test message')

    @patch('syslog.syslog')
    def test_log_logtag(self, mock_syslog):
        # if a log tag is configured, messages should include it
        self.logger.syslog_name = 'test_runner'
        self.logger.log_to_syslog = True
        self.logger.log_to_stdout = False  # makes the test runner noisy
        self.logger.log(legacy.DEBUG, 'test message')
        mock_syslog.assert_called_once_with('test_runner: D: test message')

    @patch('syslog.syslog')
    def test_log_to_stdout(self, mock_syslog):
        # In this test syslog is patched purely to avoid accidental
        # leakage, not because we're actually testing it
        self.logger.log_to_stdout = True
        with patch('sys.stderr', new=StringIO()) as out:
            self.logger.log(legacy.DEBUG, 'test message')
        self.assertEqual(out.getvalue(), "D: test message\n")

    @patch('syslog.syslog')
    def test_log_not_to_stdout_or_syslog(self, mock_syslog):
        self.logger.log_to_stdout = False
        self.logger.log_to_syslog = False
        with patch('sys.stderr', new=StringIO()) as out:
            self.logger.log(legacy.DEBUG, 'test message')
        self.assertEqual(out.getvalue(), "")
        self.assertFalse(mock_syslog.called)

    @patch('syslog.syslog')
    def test_log_level_too_high(self, mock_syslog):
        # Test that calling log with a higher log level
        # than we are sensitive to results in no output
        self.logger.log_level = legacy.INFO
        self.logger.log_to_syslog = True
        self.logger.log_to_stdout = True
        with patch('sys.stderr', new=StringIO()) as out:
            self.logger.log(legacy.DEBUG, 'test message')
        self.assertNotEqual(out.getvalue(), "D: test message")
        self.assertFalse(mock_syslog.called)
