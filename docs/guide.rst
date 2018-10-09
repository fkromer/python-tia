.. _guide:

User's Guide
============

Compatibility
-------------

Right now `python-tia` supports development machines and CI environments running an UNIX operating system only.

How does it work?
-----------------

`python-tia` support two main use cases. The usage in a local development
environment and the usage in a CI environment.

The typical scenario/processing logic in the local development environment use case is as follows:

* The developer installs and configures `python-tia`.
* The developer changes one or several files.
* The developer calls `tia`.
* `tia` detects the runtime environment based on environment
  variables and sets the file scope change detection strategy to
  `mime`.
* The file scope changes are detected using the `mime` module.
* Changed files are input for `semantic` module
  which determines affected pipelines based on *pipeline*
  definitions in *semantic map*.
* For every affected test tool *pipeline* it is checked if a *full-scope or
  partial-scope execution* has to be triggered or not (based on files
  configured in the *semantic map*).

  * *Full-scope execution*: The corresponding command
    is executed and the pipeline specific *coverage map* recreated.
    The *impact map* is recreated based on the recreated *coverage map*.
  * *Partial-scope execution*: Tests which have to be executed are
    determined based on the changed and configured test code files,
    the changed and configured production code files and the *impact map*.
    Every test is executed separatelly and the *coverage map*
    updated on a per test basis (test -> executed production code).
    The *impact map* is recreated based on the
    updated *coverage map* (updated production code -> tests).

* For every affected analysis tool pipeline the corresponding command
  is executed considering the changed production code and configuration files only.

The typical scenario/processing logic in the CI environment use case is as follows:

* The developer installs and configures `python-tia`.
* The developer pushes commits to a git repository branch.
* The triggered CI job calls `tia`.
* `tia` detects the runtime environment based on environment
  variables and sets the file scope change detection strategy to
  `git`.
* The file scope changes are detected using the `git` module.
* Same as above for the "local development environment" use case...

Installation
------------

User-level installation:

.. code-block:: python

   $ pip3 install --user 

Project-level installation (here: with `pipenv`):

.. code-block:: python

   $ cd <project-root>
   $ pipenv install python-tia

Configuration
-------------

Semantic mapping of test tools
..............................

`tia` depends on the definition of semantic mappings between tools and files in its configuration file `tia.yaml`.
This section shows an exemplary semantic mapping for a Python package which uses the test runner `pytest` to execute tests.

Consider a Python package test file structure like follows:

.. code-block:: yaml

   package
       tests
           conftest.py 
           fixtures.py
           utils.py
           test_group1
               test_file1.py
               test_file2.py
           test_group2
               test_file1.py
               test_file2.py
       pytest.ini

A *full-scope execution* (of all tests) needs to be triggered whenever one of the files
`pytest.ini`, `tests/conftest.py`, `tests/fixtures.py` or `tests/utils.py` has changed.

A *partial-scope execution* (of the minimal possible subset of tests) is sufficient
whenever one of the files in the directories `tests/test_group1`, `tests/test_group2`
or any corresponding production code files in the *impact map* has changed.

A suitable pipeline configuration which executes `pytest` for the given project structure
could be defined with the following semantic mapping.

.. code-block:: yaml

   [pipeline:pytest]
   dirs =
       - tests/test_group1/
       - tests/test_group2/
   files =
       - pytest.ini
         full-scope: True
       - tests/utils.py
         full-scope: True
       - tests/conftest.py
         full-scope: True
    full-scope-command: <command one would use w.o. python-tia>
    partial-scope-command: <command with file and placeholder for test dirs/files>

The default value for the execution scope is *partial-scope*.
*Full-scope execution* is indicated on a (recursive) directory/file basis with the
`full-scope` option.

Semantic mapping of static analysis tools
.........................................

This section shows exemplary semantic mappings for common static analysis tools in Python application development.

Trigger the static analysis pipeline for `hadolint` in case either the
config file `hadolint.yaml` or the docker file `Dockerfile` changes.

.. code-block:: yaml

   [pipeline:hadolint]
   files =
       - hadolint.yaml
       - Dockerfile
   command = hadolint --config hadolint.yaml Dockerfile

Trigger the static analysis of the manifest file with `check-manifest`_ in case the `MANIFEST.in` changes.

.. code-block:: yaml

    [pipeline: check-manifest]
    file = MANIFEST.in
    command = check-manifest

.. _check-manifest: https://github.com/mgedmin/check-manifest

Impact mapping
--------------

TODO

Coverage mapping
----------------

TODO

A *coverage map* descibes which production code is executed by which test code.
Independent of the programming language this information is gathered using *dynamic analysis*.
For coverage analysis the tests are executed which executes specific parts of the production code.
The coverage information gathered from a tool can vary. In the best case one gets some mapping of
single tests vs. language agnostic, granular production code entities like the following:

 * 

In case of the Python programming language (the language this package is primarily made for)
the best granularity one can think of would be something like the following:
