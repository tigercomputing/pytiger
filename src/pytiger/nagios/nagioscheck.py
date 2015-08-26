# -*- coding: utf-8 -*-

# Copyright © 2015 Tiger Computing Ltd
# This file is part of pytiger and distributed under the terms
# of a BSD-like license
# See the file COPYING for details

import six
import sys


class NagiosCheck(object):
    """
    .. versionadded:: 1.0.0

    Abstracts a basic NRPE state machine
    so that a check can be reduced to its payload only.

    The state machine starts at **STATE_UNSET** indicating that the
    check has not yet expressed any status (if the check existed at
    this point, the exit code would be equivalent to Nagios 'unknown').

    The four other states, **STATE_OK**, **STATE_WARN**, **STATE_CRIT**
    and **STATE_UNKN** correspond to the Nagios values 'OK', 'warn',
    'critical' and 'unknown' respectively.

    States are sticky and transitions follow defined rules, so (for
    example) a check which has asserted 'critical' status cannot later
    rescind that and assert that it is only 'warning' after all.

    Programs *must* call :func:`exit` to return the correct
    error code. Optional messages can be queued up and will be printed
    by :func:`exit` for consumption by the user.

    Example usage:

    >>> n = NagiosCheck()
    >>> n.ok('Everything is fine')
    >>> n.exit()
    """

    # Note: these are subtly different to exit codes
    STATE_UNSET = 0
    STATE_OK = 1
    STATE_UNKN = 2
    STATE_WARN = 3
    STATE_CRIT = 4

    # Exit codes, in index order of state
    _exit_codes = [3, 0, 3, 1, 2]

    def __init__(self):
        self._state = self.STATE_UNSET
        self._messages = []

    def append(self, string):
        if string:
            self._messages.append(string)

    @property
    def state(self):
        """Current state of the check"""
        return self._state

    @property
    def messages(self):
        """List of queued messages"""
        return self._messages

    def _transition(self, newstate, message=None):
        if message:
            self.append(message)
        # The test here, unless unset, is "newstate greater than oldstate"
        # (so we think of it as "more bad")
        # This does mean we have to play games in exit() though
        if newstate >= self._state:
            self._state = newstate
            return True
        else:
            return False

    def ok(self, message=None):
        """
        If the current state is unset, set it to **STATE_OK**
        (indicating that the check is within acceptable parameters)
        """
        return self._transition(self.STATE_OK, message)

    def warn(self, message=None):
        """
        If the current state is unset or not worse than 'warning',
        set it to **STATE_WARN** (indicating that the check is
        outside acceptable parameters, but not service-affecting)
        """
        return self._transition(self.STATE_WARN, message)

    def critical(self, message=None):
        """
        Set the current state to **STATE_CRIT** from any other
        state (indicating that the check is outside acceptable
        parameters and affecting service). This trumps all other
        states and is sticky.
        """
        return self._transition(self.STATE_CRIT, message)

    def unknown(self, message=None):
        """
        If the current state is unset or not worse than 'OK',
        set it to **STATE_UNKN** (indicating that some internal
        error means the check cannot be sure of the current
        situation).
        """
        return self._transition(self.STATE_UNKN, message)

    def exit(self):
        """Print the queued messages and exit with an appropriate
        exit code (this is the basis for the Nagios status)"""
        if self.state == self.STATE_UNSET and not self.messages:
            self.append('UNKNOWN: No state asserted')
        six.print_(', '.join(self.messages))
        sys.exit(self._exit_codes[self.state])


