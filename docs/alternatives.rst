.. _alternatives:

Potential alternatives to `python-tia`
======================================

This section summarizes the evaluation of Python packages which could potentially have been used instead of `python-tia`
and packages which could be used to implement `python-tia` s features.
At time of writing (August 2018) existing package provide single but not all required features.
The functionality is not provided in a generic way, tightly coupled to the Python language
and a specific Python test runner (`pytest` and `nose`).
The packages implement single features sometimes using very different approaches which
are used as design input for the implementation in `python-tia`.

pytest-testmon
--------------

Sources: `pytest-testmon (github)`_

Package: `pytest-testmon (pypi)`_

Evaluation result: No option due to `pytest` test runner dependency.

`pytest-testmon` is a `pytest` plugin which automatically selects and re-executes only tests affected by recent changes.
File scope changes are determined based on hash using `hashlib` and `zlib.adler32()`. `ast` is used to generate Python language aware change interpretation.
For coverage tracking `coveragpy` is used. Subprocess coverage tracking requires manual installation of `coverage-pth`.
The standard lib module `ast` is used to create an abstract representation of the source code as input for 
`pytest-testmon` can be used with `pytest-watch` to trigger its execution automatically.

.. _pytest-testmon (github): https://github.com/tarpas/pytest-testmon
.. _pytest-testmon (pypi): https://pypi.org/project/pytest-testmon

when-changed
------------

Sources: `when-changed (github)`_

Evaluation result: No option due to limited capabilities.

*when-changed* is a command line tool which executes commands when a directories or files have changed.
File changes are detected continuously using `watchdog (github)`_ :code:`class watchdog.events.FileSystemEventHandler()`
(https://github.com/joh/when-changed/blob/master/whenchanged/whenchanged.py#L36) and
:code:`watchdog.observers.Observer()`.

.. _when-changed (github): https://github.com/joh/when-changed
.. _watchdog (github): https://github.com/gorakhargosh/watchdog

watchdog
--------

Sources: `watchdog (github)`_

Documentation: `watchdog (docs)`_

Package: `watchdog (pypi)`_

*watchdog* provides various filesystem observers: an OS native filesystem observer (https://pythonhosted.org/watchdog/api.html#module-watchdog.observers),
a polling observer (https://pythonhosted.org/watchdog/api.html#module-watchdog.observers.polling), etc.
Observers trigger event handlers (https://pythonhosted.org/watchdog/api.html#event-handler-classes)
in case of various filesystem events (https://pythonhosted.org/watchdog/api.html#event-classes).

.. _watchdog (docs): https://pythonhosted.org/watchdog
.. _watchdog (github): https://github.com/gorakhargosh/watchdog
.. _watchdog (pypi): https://pypi.org/project/watchdog

pytest-picked
-------------

Sources: `pytest-picked (github)`_

Package: `pytest-picked (pypi)`_

Evaluation result: No option due to *pytest* test runner dependency.

`pytest-picked` is a `pytest` plugin which makes use of `git`. It does not create a *coverage map* and
*impact map*. Instead it uses :code:`git status --short` (`git` wrapped via `subprocess`) to
determine test files and folders which have been changed locally.

.. _pytest-picked (github): https://github.com/anapaulagomes/pytest-picked
.. _pytest-picked (pypi): https://pypi.org/project/pytest-picked

pytest-knows
------------

Sources: `ptknows (github)`_

Package: `pytest-knows (pypi)`_

Evaluation result: No option due to `pytest` test runner dependency.

`pytest-knows` is a `pytest` plugin which makes use of `trace`_ and :code:`stat.ST_MTIME` (https://docs.python.org/2/library/stat.html#stat.ST_MTIME) (time of last file modification).
During setup of `pytest` via the `pytest` hook  :code:`pytest_configure()` (https://github.com/mapix/ptknows/blob/master/ptknows.py#L47) it opens an UNIX database via the Python 2 `dbm <https://docs.python.org/2/library/dbm.html>`_ interface
(in Python 3 the module has been renamed to `dbm.ndbm <https://docs.python.org/3.7/library/dbm.html#module-dbm.ndbm>`_ ).
Before `pytest` runs a single test `pytest-knows` hooks into there via the `pytest` hook :code:`pytest_runtest_call()` (https://github.com/mapix/ptknows/blob/master/ptknows.py#L55).
It is checked if dependency info for this test (mapping of test to executed production code files) has been stored into the database before.
If there is info available and the last modification time of the production code file corresponding to the test has not changed the test is skipped.
In case there is no dependency info or the last modification time of one of the tests associated production code files has changed the test is executed.
During test execution trace info is gathered and the dependency information for the test (mapping of test to executed production code files) stored in the database.
After execution the databaes is closed via `pytest` hook :code:`pytest_unconfigure()` (https://github.com/mapix/ptknows/blob/master/ptknows.py#L51).

.. _ptknows (github): https://github.com/mapix/ptknows
.. _pytest-knows (pypi): https://pypi.org/project/pytest-knows

nose-knows
----------

Sources: `nose-knows (github)`_

Package: `nose-knows (pypi)`_

Evaluation result: No option due to `nose` test runner dependency.

`nose-knows` is a `nose` plugin with experimental support for `pytest`.
The *coverage map* (`.knows` file) maps production code on the file level vs. tests (created in "output mode", cmd line option :code:`--knows-out`).
In :code:`Knows.begin()` (https://github.com/eventbrite/nose-knows/blob/master/src/knows/base.py#L58) it makes use of :code:`threading.settrace(self.tracer)`
with the tracer function :code:`Knows.tracer()` (https://github.com/eventbrite/nose-knows/blob/master/src/knows/base.py#L63) to trace the production code executed during tests.
:code:`begin()` is integrated into the test runner processing procedure for `nose` via :code:`KnowsNosePlugin.begin()`
(https://github.com/eventbrite/nose-knows/blob/master/src/knows/nose_plugin.py#L105>`_, for
`pytest` via :code:`pytest_sessionstart()` (https://github.com/eventbrite/nose-knows/blob/master/src/knows/pytest_plugin.py#L94>).
The trace context for particular tests is determined via :code:`Knows.start_test()` (https://github.com/eventbrite/nose-knows/blob/master/src/knows/base.py#L84)
which is called in the plugins via the corresponding test runner hooks for `nose` via :code:`KnowsNosePlugin.startTest()` (https://github.com/eventbrite/nose-knows/blob/master/src/knows/nose_plugin.py#L108),
for `pytest` via :code:`pytest_runtest_protocol()` (https://github.com/eventbrite/nose-knows/blob/a647cc1f82984522f728ccc83145c774f4756197/src/knows/pytest_plugin.py#L99).
In "input mode" the *coverage map* (`.knows` file) is used to generate the *impact map* dynamically :code:`Knows.get_tests_to_run()`
(https://github.com/eventbrite/nose-knows/blob/3ac3cfc81c7d3bc7beaf2b533ab37a0bbf132779/src/knows/base.py#L26) for a production code file and to selectivelly run tests for it.

.. _trace: https://docs.python.org/2/library/trace.html
.. _nose-knows (github): https://github.com/eventbrite/nose-knows 
.. _nose-knows (pypi): https://pypi.org/project/nose-knows

"testimpact" script
-------------------

Sources: `samplemod (github)`_

Paul Hammant presented a proof of concept script for TIA in his `blog post about samplemod`_ "Reducing Test Times by Only Running Impacted Tests - Python Edition".
The script :code:`testimpact.sh` (https://github.com/paul-hammant/samplemod/blob/master/testimpact.sh) determines the test files using
:code:`ack` (https://github.com/paul-hammant/samplemod/blob/master/testimpact.sh#L7), runs every test with :code:`nosetest`
(https://github.com/paul-hammant/samplemod/blob/master/testimpact.sh#L15), determines which production code is executed by each test and
writes the *coverage map* into meta data directory `meta/` (directory :code:`meta/tests` (https://github.com/paul-hammant/samplemod/tree/master/meta/tests)
and :code:`meta/tests2` (https://github.com/paul-hammant/samplemod/tree/master/meta/tests2).
The resulting *impact map* (production code vs. test code which executes the production code) ends up in :code:`meta/impact-map.txt`
(https://github.com/paul-hammant/samplemod/blob/master/meta/impact-map.txt).

.. _samplemod (github): https://github.com/paul-hammant/samplemod
.. _blog post about samplemod: https://paulhammant.com/2015/01/18/reducing-test-times-by-only-running-impacted-tests-python-edition
