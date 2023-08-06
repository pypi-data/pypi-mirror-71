====================================
pytest-unhandled-exception-exit-code
====================================

Plugin for ``pytest`` to change exit code on uncaught exceptions

* Free software: MIT license

Features
--------

* You can set a different exit code when uncaught exceptions in ``pytest`` test
  cases will occur


Installation
------------

You can install the plugin by running

    pip install pytest-unhandled-exception-exit-code

Alternately check out the source code and run

    python setup.py install


Usage
-----

If you want to change `pytest` exit code to detect unhandled exceptions in
tests, give the plugin the desired exit code with the following option:
``pytest --unhandled-exc-exit-code 13``
