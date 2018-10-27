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

Run the `tox` default environments in the virtualenv.

.. code-block:: python

   $ tox
