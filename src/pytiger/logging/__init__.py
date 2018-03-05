"""
`pytiger` uses the Python logging framework to generate messages and
bubble them up through to handlers.

The legacy :class:`pytiger.logging.legacy.LegacySyslogger` class replicates
old behaviour for a managed transition to the full framework. It should not
be used for new works.

Quick Start
-----------

The following snippet will cater for most simple uses.

>>> import logging
>>> pytiger.logging.config.basic_config(level=logging.WARNING)
>>> log = logging.getLogger(__name__)
>>> log.info('This entry will not appear')
>>> log.warning('Unable to biggle')
W: Unable to biggle
>>> log.error('Abandon ship, all ye who run this')
E: Abandon ship, all ye who run this
"""

__all__ = ['legacy']
