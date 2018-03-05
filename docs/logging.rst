*******
Logging
*******

.. automodule:: pytiger.logging

:mod:`pytiger.logging.config` -- Configure Python logging
=========================================================

.. automodule:: pytiger.logging.config
   :synopsis: Configure the Python logging system following Tiger conventions
   :members:

:mod:`pytiger.logging.syslog` -- Syslog logging handler
=======================================================

.. automodule:: pytiger.logging.syslog
   :synopsis: Syslog logging handler for Python logging framework
   :members:

:mod:`pytiger.logging.legacy` -- Legacy logging module
======================================================

.. automodule:: pytiger.logging.legacy
   :synopsis: Legacy logging utilities
   :deprecated:

.. autoclass:: LegacySyslogger

   .. autoattribute:: log_level
   .. autoattribute:: log_to_stdout
   .. autoattribute:: log_to_syslog

   .. automethod:: log
   .. automethod:: debug
   .. automethod:: error
   .. automethod:: info
   .. automethod:: warning
