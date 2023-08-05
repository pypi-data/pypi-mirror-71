=========
lo99ing
=========

Python logging, configured the way I like it.


Logger Behavior
====================================

Default behavior when using ``lo99ing``:

- logs to stderr only
- log level (of each individual logger) defaults to:

 - WARNING for "installed" modules (site-packages and dist-packages)
 - INFO for "local" modules (in user's local dev env)

- message format: ``%(asctime)s:%(levelname)s:%(name)s: %(message)s``


Message Logging Behavior
====================================

- ``logger.exception()`` automatically extracts and prints exception attributes
- When logging an exception object, automatically adds exception type:

 - ``logger.error('exception raised: %s', KeyError(0))  # prints: 'exception raised: KeyError -- 0'``

- if logging messages fails formatting, also logs the location of the problematic call:

 - ``logger.info('forgot the percent sign', 555)  # includes: 'Logged from /path/to/file.py:LINENUM'``


Usage and Other Features
====================================

- Get a logger using ``get_logger(logger_name, ...)``
- Get a logger with current module's (or script's) basename using: ``get_logger(__file__)``
- Log to a file, using ``enable_file(filename)``
- Create an "independent" (i.e., ``propagate=False``) file-logger, using ``get_file_logger(filename)``
- Disable/re-enable logging to stderr (on root logger), using ``enable_stderr()`` and ``disable_stderr()``
- Change logging clock "converter" to UTC using ``use_utc()``
- Change logging clock to a custom clock using ``use_clock(clock)``

 - This is useful when "replaying past events", and you want timestamps to appear accordingly

- log-level overrides: set and reset ("undo") log levels using overrides:

 - ``logger.set_log_level_override(level)`` or ``set_log_level_override(name, level)``,
 - reset using ``set_log_level_override(name, None)``

- Create a logger-like object, which adds a prefix to messages it logs, using ``logger.prefixed('PREFIX:')``
- Log a "trace" message with current filename and line number, using ``logger.TRACE()``

 - useful for "tracing" / "printf-debugging"


Usage Notes
====================================

- Should avoid using ``logging.getLogger()`` directly.  Instead, use ``lo99ing.get_logger()``
- Should not use ``logger.setLevel()`` directly.  Instead, use
  ``get_logger(..., level=LEVEL, ...)`` or ``set_log_level_override()``



Installation
====================================

Using pip::

    pip install lo99ing
