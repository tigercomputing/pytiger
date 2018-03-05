# -*- coding: utf-8 -*-

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import unittest
from mock import patch
from .monitoringcheck import MonitoringCheck
from six import StringIO


class TestMonitoringCheck(unittest.TestCase):

    def setUp(self):
        self.n = MonitoringCheck()

    # Check deprecated function calls the real thing
    @patch('warnings.warn')
    def test_deprecated_warn(self, mock_warn):
        self.n.warn()
        self.assertTrue(mock_warn.called)
        self.assertEqual(self.n.STATE_WARN, self.n.state)

    ####################
    @patch('sys.exit')
    def test_exit_unset(self, mock_exit):
        self.n.exit()
        mock_exit.assert_called_once_with(3)

    @patch('sys.exit')
    def test_exit_ok(self, mock_exit):
        self.n.ok()
        self.n.exit()
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    def test_exit_warning(self, mock_exit):
        self.n.warning()
        self.n.exit()
        mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    def test_exit_critical(self, mock_exit):
        self.n.critical()
        self.n.exit()
        mock_exit.assert_called_once_with(2)

    @patch('sys.exit')
    def test_exit_messages(self, mock_exit):
        self.n.append('line 1')
        self.n.append('line 2')
        with patch('sys.stdout', new=StringIO()) as out:
            self.n.exit()
        output = out.getvalue().strip()
        self.assertEquals(output, 'line 1, line 2')

    @patch('sys.exit')
    def test_exit_messages_custom_separator(self, mock_exit):
        self.n.append('line 1')
        self.n.append('line 2')
        with patch('sys.stdout', new=StringIO()) as out:
            self.n.exit(separator=";")
        output = out.getvalue().strip()
        self.assertEquals(output, 'line 1;line 2')
        with patch('sys.stdout', new=StringIO()) as out:
            self.n.exit(separator="\n")
        output = out.getvalue().strip()
        self.assertEquals(output, 'line 1\nline 2')

    @patch('sys.exit')
    def test_exit_unset_nomessages(self, mock_exit):
        with patch('sys.stdout', new=StringIO()) as out:
            self.n.exit()
        output = out.getvalue().strip()
        self.assertEquals(output, 'UNKNOWN: No state asserted')
        mock_exit.assert_called_once_with(3)

    ####################
    def test_messages_append(self):
        self.assertEqual(self.n.messages, [])
        self.n.append('line 1')
        self.assertEqual(self.n.messages, ['line 1'])
        self.n.append('line 2')
        self.assertEqual(self.n.messages, ['line 1', 'line 2'])

    def test_message_append_blank(self):
        self.assertEqual(self.n.messages, [])
        self.n.append('')
        self.assertEqual(self.n.messages, [])

    ####################
    # State
    def test_state(self):
        self.assertEqual(self.n.STATE_UNSET, self.n.state)
        self.n.ok()
        self.assertEqual(self.n.STATE_OK, self.n.state)
        self.n.unknown()
        self.assertEqual(self.n.STATE_UNKN, self.n.state)
        self.n.warning()
        self.assertEqual(self.n.STATE_WARN, self.n.state)
        self.n.critical()
        self.assertEqual(self.n.STATE_CRIT, self.n.state)

    ####################
    # Shortcut functions
    # Tests do not check that the transition is valid,
    # only that _transitio() was called wih the right params
    # (We test the transitions separately)
    @patch('pytiger.monitoring.MonitoringCheck._transition')
    def test_shortcut_ok(self, mock_transition):
        self.n.ok('message')
        mock_transition.assert_called_once_with(self.n.STATE_OK, 'message')

    @patch('pytiger.monitoring.MonitoringCheck._transition')
    def test_shortcut_unknown(self, mock_transition):
        self.n.unknown('message')
        mock_transition.assert_called_once_with(self.n.STATE_UNKN, 'message')

    @patch('pytiger.monitoring.MonitoringCheck._transition')
    def test_shortcut_warning(self, mock_transition):
        self.n.warning('message')
        mock_transition.assert_called_once_with(self.n.STATE_WARN, 'message')

    @patch('pytiger.monitoring.MonitoringCheck._transition')
    def test_shortcut_critical(self, mock_transition):
        self.n.critical('message')
        mock_transition.assert_called_once_with(self.n.STATE_CRIT, 'message')

    ####################
    def test_transitions_unset(self):
        this_state = self.n.STATE_UNSET
        valid_targets = (this_state, self.n.STATE_UNKN, self.n.STATE_OK,
                         self.n.STATE_WARN, self.n.STATE_CRIT)
        for t in valid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)

    def test_transitions_unknown(self):
        this_state = self.n.STATE_UNKN
        valid_targets = (this_state, self.n.STATE_OK, self.n.STATE_WARN,
                         self.n.STATE_CRIT)
        invalid_targets = (self.n.STATE_UNSET,)
        for t in valid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)

    def test_transitions_ok(self):
        this_state = self.n.STATE_OK
        valid_targets = (this_state, self.n.STATE_UNKN, self.n.STATE_WARN,
                         self.n.STATE_CRIT)
        invalid_targets = (self.n.STATE_UNSET,)
        for t in valid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)

    def test_transitions_warning(self):
        this_state = self.n.STATE_WARN
        valid_targets = (this_state, self.n.STATE_CRIT,)
        invalid_targets = (self.n.STATE_UNSET, self.n.STATE_UNKN,
                           self.n.STATE_OK)
        for t in valid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)

    def test_transitions_critical(self):
        this_state = self.n.STATE_CRIT
        valid_targets = (this_state,)
        invalid_targets = (self.n.STATE_UNSET, self.n.STATE_UNKN,
                           self.n.STATE_OK)
        for t in valid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = MonitoringCheck()  # Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)

    def test_transition_with_message(self):
        self.assertEqual(self.n.messages, [])
        # Transition to ok with a message
        # this test is NOT about the transition, only
        # the message handling
        self.n._transition(self.n.STATE_OK, 'some message')
        self.assertEqual(self.n.messages, ['some message'])
