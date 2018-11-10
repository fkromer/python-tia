.. _contributing:

Contributor's Guide
===================

The following commands assume that you are working with a development machine providing Python 3
as (active) system/user level Python interpreter with `pip3` and `pipenv` installed.

Create a virtualenv using `pipenv`.

.. code-block:: python

   $ pipenv install --dev

Enter the virtualenv.

.. code-block:: python

   $ pipenv shell

Exploratory development using `jupyter lab`.

.. code-block:: python

   $ jupyter lab

Exploratory SQLite database development (coverage.py coverage data) using `sqlitebrowser`.

   $ sudo apt-get install sqlitebrowser
   $ pipenv run tox -e pytest
   $ sqlitebrowser .coverage

Merge explored functionality into IDE of your choice (e.g. `vim`, note: no project specific `.vimrc` provided).

.. code-block:: python

   $ vim

Run `tox` environments (`pytest`, `mypy`, etc. refer to `tox.ini`) relevant during development.

.. code-block:: python

   $ tox -e pytest

Finally run all `tox` default environments (refer to `tox.ini`) in the virtualenv.

.. code-block:: python

   $ tox

Leave virtualenv.

.. code-block:: python

   $ exit
