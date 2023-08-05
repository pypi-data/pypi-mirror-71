===========
rcs-storage
===========

Copyright © 2020 - The University of Melbourne.

BETA only - use in production environments at your own risk.

Installation
============

::

  pip install rcs-storage

Usage
=====

Command Line
------------

For example::

  rcs-storage collection list

For help::

  rcs-storage collection list -h

You may set the following environment variables so you don't have to pass
``--token`` and/or ``--host`` to the command every time you run it::

  export RCS_STORAGE_HOST=https://<hostname>/
  export RCS_STORAGE_TOKEN=<your token>

Python
------

For example::

  from rcs_storage.client import Client

  storage = Client(host=<host>, token=<token>)
  storage.collections.list()




Distribution
------------

PyPi project is located here: https://pypi.org/project/rcs-storage/.

Bump version number.

Install::

  python3 -m pip install --user --upgrade setuptools wheel twine

Build::

  python3 setup.py sdist bdist_wheel

Upload::

  python3 -m twine upload --repository pypi dist/*
