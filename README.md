# python-tia


[![PyPI version](https://badge.fury.io/py/python-tia.svg)](https://badge.fury.io/py/python-tia)
[![GitHub license](https://img.shields.io/github/license/fkromer/python-tia.svg)](https://github.com/fkromer/python-tia/blob/master/LICENSE)
[![Read the Docs](https://img.shields.io/readthedocs/pip.svg)](https://python-tia.readthedocs.io)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/fkromer)

The command line application `tia` is a generic and flexible Test Impact Analysis (TIA) preprocessor for test tools.

## Reasons for python-tia

- Triggering test execution in a Test Driven Development (TDD) manner on a developer machine may be annoying because tests need to be selected explicitly for execution. *"As a developer I want to call `tia` that the recently changed tests on my dev machine are selected for execution."*
- Test execution time on a developer machine may be that long that it prevents from adapting an effective Test Driven Development (TDD) workflow. In the worst case executing tests becomes that annoying that it is skipped completely. *"As a developer I want to call `tia` that the minimal possible sub-set of tests is selected for execution."*
- It may not be obvious what tests need to be executed after production code was changed. *As a developer I want to call `tia` that the tests are selected for execution which corresponds to the recently changed production code on my dev machine.*
- Running analyzers in a Test Driven Development (TDD) manner may be annoying because it's not always obvious if they need to be run at all and in case they should over which files they should run. *As a developer I want to call `tia` that the recently changed production code on my dev machine is selected for analyzation if required.*
- Running analyzers over more files than required is (usually not critical but anyway) a waste of time . *As a developer I want to call `tia` that the minimal possible sub-set of files is considered for analysis.*

## Features

- **semantic mapping**: `tia` let's you semantically map directories and files to test and analysis tools in a *semantic map*.
- **determination of file changes**: `tia` determines changes to the production and test code of Python projects which is under version control.
- **coverage mapping**: `tia` traces which production code is executed by every single test via dynamic analysis and keeps track of it in a *coverage map* (production code vs. test code).
- **impact mapping**: `tia` determines for every production code change which tests need to be executed to catch possible regressions and keeps track of it in a *impact map*.

## Design

### Git interaction

- git ([ducumentation](https://git-scm.com/doc) / [source code](https://github.com/git/git))
- Dulwich ([ducumentation](https://www.dulwich.io/) / [source code](https://github.com/dulwich/dulwich))

  "Dulwich is a Python implementation of the Git file formats and protocols, which does not depend on Git itself."

- GitPython ([documentation](http://gitpython.readthedocs.io/en/stable/) / [source code](https://github.com/gitpython-developers/GitPython))

  "GitPython is a python library used to interact with git repositories, high-level like git-porcelain, or low-level like git-plumbing."

### Semantic diff

No tools known which could be used for semantic diffs.

> Alternatives evaluated but not suitable:
> - [Semantic Diff](https://github.com/hoelzro/semantic-diff) is highly experimental and doesn't support Python 3.
> - [SemanticMerge](https://www.semanticmerge.com/) is commercial and doesn't support Python 3.
> - [Smart Differencer](http://www.semanticdesigns.com/Products/SmartDifferencer/index.html) is commercial and
> doesn't support Python 3 (only Python 2.6).

## Other Python packages implementing TIA

Right now there is a proof of concept using scripts and 2 Python packages which implement TIA. Each solution is implementing
TIA functionality to some degree and not generically (both packages depend on `pytest`).

### "testimpact" script (no package, proof of concept scripts)

Sources: [github.com/paul-hammant/samplemod](https://github.com/paul-hammant/samplemod)

Paul Hammant presented a proof of concept in his blog ["Reducing Test Times by Only Running Impacted Tests - Python Edition"](https://paulhammant.com/2015/01/18/reducing-test-times-by-only-running-impacted-tests-python-edition/). The script [`testimpact.sh`](https://github.com/paul-hammant/samplemod/blob/master/testimpact.sh) determines the test files using [`ack`](https://github.com/paul-hammant/samplemod/blob/master/testimpact.sh#L7), runs every test with [`nosetest`](https://github.com/paul-hammant/samplemod/blob/master/testimpact.sh#L15), determines which production code is executed by each test and writes the "coverage map" into meta data directory `meta/` (directory [meta/tests](https://github.com/paul-hammant/samplemod/tree/master/meta/tests) and [meta/tests2](https://github.com/paul-hammant/samplemod/tree/master/meta/tests2)). The resulting "impact map" (production code vs. test code which executes the production code) ends up in [`meta/impact-map.txt`](https://github.com/paul-hammant/samplemod/blob/master/meta/impact-map.txt).

### pytest-picked

Sources: [github.com/anapaulagomes/pytest-picked](https://github.com/anapaulagomes/pytest-picked)

Package: [pypi.org/pytest-picked](https://pypi.org/project/pytest-picked/)

`pytest-picked` is a `pytest` plugin which makes use of `git`. It does not create a coverage map and
impact map. Instead it uses `git status --short` (command line `git` wrapped with `subprocess`) to
determine test files and folders which have been changed locally.

## pytest-knows

Sources: [github.com/mapix/ptknows](https://github.com/mapix/ptknows)

Package: [pypi/pytest-knows](https://pypi.org/project/pytest-knows/)

`pytest-knows` is a `pytest` plugin which makes use of [`trace`](https://docs.python.org/2/library/trace.html) and [`stat.ST_MTIME`](https://docs.python.org/2/library/stat.html#stat.ST_MTIME) (time of last file modification).
During setup of `pytest` via the `pytest` hook  [`pytest_configure()`](https://github.com/mapix/ptknows/blob/master/ptknows.py#L47) it opens an UNIX database [via the Python 2 `dbm` interface](https://docs.python.org/2/library/dbm.html) (in Python 3 the module has been renamed to [`dbm.ndbm`](https://docs.python.org/3.7/library/dbm.html#module-dbm.ndbm)).
Before `pytest` runs a single test `pytest-knows` hooks into there via the `pytest` hook [`pytest_runtest_call()`](https://github.com/mapix/ptknows/blob/master/ptknows.py#L55)).
It is checked if dependency info for this test (mapping of test to executed production code files) has been stored into the database before.
If there is info available and the last modification time of the production code file corresponding to the test has not changed the test is skipped.
In case there is no dependency info or the last modification time of one of the tests associated production code files has changed the test is executed.
During test execution trace info is gathered and the dependency information for the test (mapping of test to executed production code files) stored in the database.
After execution the databaes is closed via `pytest` hook [`pytest_unconfigure()`](https://github.com/mapix/ptknows/blob/master/ptknows.py#L51).

## nose-knows


Sources: [github.com/eventbrite/nose-knows](https://github.com/eventbrite/nose-knows)

Package: [pypi/nose-knows](https://pypi.org/project/nose-knows/)

`nose-knows` is a `nose` plugin with experimental support for `pytest`.
The *coverage map* (`.knows` file) maps production code on the file level vs. tests (created in "output mode", cmd line option `--knows-out`).
In [`Knows.begin()`](https://github.com/eventbrite/nose-knows/blob/master/src/knows/base.py#L58) it makes use of `threading.settrace(self.tracer)`
with the tracer  function [`Knows.tracer()`](https://github.com/eventbrite/nose-knows/blob/master/src/knows/base.py#L63) to trace the production code executed during tests. `begin()` is integrated into the test runner processing procedure
(`nose`: [`KnowsNosePlugin.begin()`](https://github.com/eventbrite/nose-knows/blob/master/src/knows/nose_plugin.py#L105), `pytest`: [`pytest_sessionstart()`](https://github.com/eventbrite/nose-knows/blob/master/src/knows/pytest_plugin.py#L94)). The trace context for particular tests is determined via [`Knows.start_test()`](https://github.com/eventbrite/nose-knows/blob/master/src/knows/base.py#L84) which is called in the plugins via the corresponding test runner hooks (`nose`: [`KnowsNosePlugin.startTest()`](https://github.com/eventbrite/nose-knows/blob/master/src/knows/nose_plugin.py#L108), `pytest`: [`pytest_runtest_protocol()`](https://github.com/eventbrite/nose-knows/blob/a647cc1f82984522f728ccc83145c774f4756197/src/knows/pytest_plugin.py#L99)).
In "input mode" the coverage map (`.knows` file) is used to generate the *impact map* dynamically [`Knows.get_tests_to_run()`](https://github.com/eventbrite/nose-knows/blob/3ac3cfc81c7d3bc7beaf2b533ab37a0bbf132779/src/knows/base.py#L26) for a production code file and to selectivelly run tests for it.