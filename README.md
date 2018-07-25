# python-tia

Test Impact Analysis (TIA) in Python.

## Design

### Git interaction

- git ([ducumentation](https://git-scm.com/doc) / [source code](https://github.com/git/git))
- Dulwich ([ducumentation](https://www.dulwich.io/) / [source code](https://github.com/dulwich/dulwich))

  "Dulwich is a Python implementation of the Git file formats and protocols, which does not depend on Git itself."

- GitPython ([documentation](http://gitpython.readthedocs.io/en/stable/) / [source code](https://github.com/gitpython-developers/GitPython))

  "GitPython is a python library used to interact with git repositories, high-level like git-porcelain, or low-level like git-plumbing."

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
