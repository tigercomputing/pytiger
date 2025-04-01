"""
`pytiger` uses the Python logging framework to generate messages and
bubble them up through to handlers.

Quick Start
-----------

The following snippet will cater for most simple uses::

    >>> import logging
    >>> import pytiger.logging.config
    >>> pytiger.logging.config.basic_config(level=logging.WARNING)
    >>> log = logging.getLogger(__name__)
    >>> log.info('This entry will not appear')
    >>> log.warning('Unable to biggle')
    W: Unable to biggle
    >>> log.error('Abandon ship, all ye who run this')
    E: Abandon ship, all ye who run this
"""
