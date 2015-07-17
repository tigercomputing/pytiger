"""
`pytiger` uses the Python logging framework to generate messages and
bubble them up through to handlers.

The legacy :class:`pytiger.logging.legacy.LegacySyslogger` class replicates
old behaviour for a managed transition to the full framework.
"""

__all__ = ['legacy']
