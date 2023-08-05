======
arklog
======

.. image:: https://img.shields.io/pypi/v/arklog.svg
        :target: https://pypi.python.org/pypi/arklog

A python logging module with colors.

Example
-------

.. code-block:: python3

    import arklog

    arklog.set_defaults()
    arklog.debug("Debug message")
    arklog.info("Info message")
    arklog.warning("Warning message")
    arklog.extra("Extra message")
    arklog.error("Error message")
    arklog.success("Success message")
