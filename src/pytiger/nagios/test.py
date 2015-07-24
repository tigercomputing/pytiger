# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import unittest
import sys
from mock import patch
from . import NagiosCheck

class TestNagiosCheck(unittest.TestCase):

    def setUp(self):
        self.n = NagiosCheck()

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
    def test_exit_warn(self, mock_exit):
        self.n.warn()
        self.n.exit()
        mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    def test_exit_critical(self, mock_exit):
        self.n.critical()
        self.n.exit()
        mock_exit.assert_called_once_with(2)

    @patch('sys.exit')
    def test_exit_messages(self, mock_exit):
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("You must run this test under Python >=2.7 for stdout redirection to work")
        self.n.append('line 1')
        self.n.append('line 2')
        self.n.exit()
        output = sys.stdout.getvalue().strip()
        self.assertEquals(output, 'line 1, line 2')

    @patch('sys.exit')
    def test_exit_unset_nomessages(self, mock_exit):
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("You must run this test under Python >=2.7 for stdout redirection to work")
        self.n.exit()
        output = sys.stdout.getvalue().strip()
        self.assertEquals(output, 'UNKNOWN: No state asserted')
        mock_exit.assert_called_once_with(3)

    ####################
    def test_messages_append(self):
        self.assertEqual(self.n.messages, [])
        self.n.append('line 1')
        self.assertEqual(self.n.messages, ['line 1'])
        self.n.append('line 2')
        self.assertEqual(self.n.messages, ['line 1', 'line 2'])

    ####################
    # State
    def test_state(self):
        self.assertEqual(self.n.STATE_UNSET, self.n.state)
        self.n.ok()
        self.assertEqual(self.n.STATE_OK, self.n.state)
        self.n.unknown()
        self.assertEqual(self.n.STATE_UNKN, self.n.state)
        self.n.warn()
        self.assertEqual(self.n.STATE_WARN, self.n.state)
        self.n.critical()
        self.assertEqual(self.n.STATE_CRIT, self.n.state)

    ####################
    # Shortcut functions
    # Tests do not check that the transition is valid,
    # only that _transitio() was called wih the right params
    # (We test the transitions separately)
    @patch('pytiger.nagios.NagiosCheck._transition')
    def test_shortcut_ok(self, mock_transition):
        self.n.ok('message')
        mock_transition.assert_called_once_with(self.n.STATE_OK, 'message')

    @patch('pytiger.nagios.NagiosCheck._transition')
    def test_shortcut_unknown(self, mock_transition):
        self.n.unknown('message')
        mock_transition.assert_called_once_with(self.n.STATE_UNKN, 'message')

    @patch('pytiger.nagios.NagiosCheck._transition')
    def test_shortcut_warn(self, mock_transition):
        self.n.warn('message')
        mock_transition.assert_called_once_with(self.n.STATE_WARN, 'message')

    @patch('pytiger.nagios.NagiosCheck._transition')
    def test_shortcut_critical(self, mock_transition):
        self.n.critical('message')
        mock_transition.assert_called_once_with(self.n.STATE_CRIT, 'message')


    ####################
    def test_transitions_unset(self):
        this_state = self.n.STATE_UNSET
        valid_targets = (this_state, self.n.STATE_UNKN, self.n.STATE_OK, self.n.STATE_WARN, self.n.STATE_CRIT)
        for t in valid_targets:
            self.n = NagiosCheck() #Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)

    def test_transitions_unknown(self):
        this_state = self.n.STATE_UNKN
        valid_targets = (this_state, self.n.STATE_OK, self.n.STATE_WARN, self.n.STATE_CRIT)
        invalid_targets = (self.n.STATE_UNSET,)
        for t in valid_targets:
            self.n = NagiosCheck() #Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = NagiosCheck() #Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)

    def test_transitions_ok(self):
        this_state = self.n.STATE_OK
        valid_targets = (this_state, self.n.STATE_UNKN, self.n.STATE_WARN, self.n.STATE_CRIT)
        invalid_targets = (self.n.STATE_UNSET,)
        for t in valid_targets:
            self.n = NagiosCheck() #Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = NagiosCheck() #Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)

    def test_transitions_warn(self):
        this_state = self.n.STATE_WARN
        valid_targets = (this_state, self.n.STATE_CRIT,)
        invalid_targets = (self.n.STATE_UNSET, self.n.STATE_UNKN, self.n.STATE_OK)
        for t in valid_targets:
            self.n = NagiosCheck() #Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = NagiosCheck() #Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)

    def test_transitions_critical(self):
        this_state = self.n.STATE_CRIT
        valid_targets = (this_state,)
        invalid_targets = (self.n.STATE_UNSET, self.n.STATE_UNKN, self.n.STATE_OK)
        for t in valid_targets:
            self.n = NagiosCheck() #Start fresh
            self.assertTrue(self.n._transition(t))
            self.assertEqual(self.n.state, t)
        for t in invalid_targets:
            self.n = NagiosCheck() #Start fresh
            self.n._state = this_state
            self.assertFalse(self.n._transition(t))
            self.assertEqual(self.n.state, this_state)
