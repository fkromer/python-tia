.. _design:

Design decisions
================

General considerations
----------------------

* Programming paradigms

 * `Functional Programming`_ is favoured to avoid dependencies on state
   and to isolates side-effects.
 * `Object Oriented Programming (OOP)`_ is avoided and used for state-less "namespacing"
   purposes and to provide possible plugin interfaces only.

* Principles

 * `Design by Contract (DbC)`_
 * `Single Responsibility Principle (SRP)`_
 * `Keep it Simple, Stupid (KISS)`_
 * `Principle of least astonishment (POLA)`_

.. _Design by Contract (DbC): https://en.wikipedia.org/wiki/Design_by_contract
.. _Functional Programming: https://en.wikipedia.org/wiki/Functional_programming
.. _Object Oriented Programming (OOP): https://en.wikipedia.org/wiki/Object-oriented_programming
.. _Keep it Simple, Stupid (KISS): https://en.wikipedia.org/wiki/KISS_principle
.. _Single Responsibility Principle (SRP): https://en.wikipedia.org/wiki/Single_responsibility_principle
.. _Principle Of Least Astonishment (POLA): https://en.wikipedia.org/wiki/Principle_of_least_astonishment

Command line interface
----------------------

*Click* is used to implement the command line interface.

* *Click*: `Click (docs)`_ (`Why click?`_)
  
  * +: nesting of commands
  * +: lazy loading of subcommands
  * ?: based on optparse
  * +: type handling and validation

Other alternatives which have been considered:

* `argparse (docs)`_ (`Why not argparse?`_)

  * ?: built-in magic to guess what is an argument or an option problematic with incomplete command lines
  * ?: does not support disabling of interspersed arguments (not possible to implement nested parsing)

* *Clint*: `clint (github)`_

  * -: archieved, last release in 2015

* *cement*: `cement (docs)`_, `cement (API reference)`_

  * ?: heavy weight (a lot is irrelevant for *python-tia*)

* *docopt*: `docopt (github)`_ , `docopt (docs)`_ (`Why not Docopt etc.?`_)
  
  * -: no rewrap of output to the current terminal width
  * -: no translations (irrelevant)
  * -: parsing only: no argument dispatching, no callback invocation, no type handling
  * -: limited composability: only subcommand dispatching, no automatic subcommand enumeration,
    consistent subcommand behaviour enforcement

.. _argparse (docs): <https://docs.python.org/3/library/argparse.html
.. _cement (docs): https://docs.builtoncement.com/
.. _cement (API reference): https://cement.readthedocs.io
.. _clint (github): https://github.com/kennethreitz/clint
.. _Click (docs): click.pocoo.org
.. _Why click?: http://click.pocoo.org/5/why/#why-click
.. _docopt (github): https://github.com/docopt/docopt
.. _docopt (docs): http://docopt.org/
.. _Why not argparse?: http://click.pocoo.org/5/why/#why-not-argparse
.. _Why not Docopt etc.?: http://click.pocoo.org/5/why/#why-not-docopt-etc

Configuration file
------------------

As configuration file format (*semantic mapping*, etc.) StrictYAML is used.
StrictYAML is a type-safe subset of YAML which enables advantages and avoids
disadvantages of YAML. Refer to `Why StrictYaml?`_ for more information about
the advantages of StrictYAML compared to other configuration file formats.
`StrictYaml`_ is used to parse and validate config input.

.. _StrictYaml: https://github.com/crdoconnor/strictyaml
.. _Why StrictYaml?: https://github.com/crdoconnor/strictyaml#why-strictyaml

Detection of changes
--------------------

Changes of the production and test code will be determined on different levels of abstraction.

Detection of file scope changes
...............................

W.r.t. `file scope state changes` (file added/modified/deleted) the approach will differ dependent
on the runtime environment (local devemlopment machine - `local`, CI server - `ci`).
There are some design choices which are based on the determination of

* filesystem metadata, e.g. time of last file change
 (choice for environment `local` only)
* filesystem events (choice for environment `local` only)
* checksums over files (choice for environment `local` as well as `ci`)
* version control system (VCS) information (choice for environment `local` as well as `ci`)

To support file scope change detection in the `ci` environment a VCS based approach is used.
It is planned to support the version control system `git` out-fo-the-box. The implementation
won't consider extensibility of VCS support (no plugin system and pre-packaged plugin approach)
in the beginning but aims at a plugin system conform API to ease probable later refactoring.
(Encapsulating VCS support into externally deployed plugins could potentially ease maintenance
over the long run.) If you are interested in contributing support for another VCS like Bazaar,
Mercurial, etc. feel free to create pull requests. The VCS functionality should be easily exchangeable
using a configuration option and strategy pattern (to exchange VCS implementations).

The capabilities and known limitations of the packages have been analyzed.
The following characteristics have been considered during evaluation:

- dependencies
- implementation of performance critical logic in C
- supported OS
- interface which would allow to implement semantid diffs

VCS (git) based detection of file scope changes
...............................................

The following alternatives have been considered to implement interaction with
the VCS `git`.

- `git` (`git documentation`_ / `git source code`_) (via `subprocess.Popen()`)
- Dulwich (`Dulwich documentation`_ / `Dulwich source code`_)

  "Dulwich is a Python implementation of the Git file formats and protocols, which does not depend on Git itself."

- GitPython (`GitPython documentation`_ / `GitPython known limitations`_ / `GitPython source code`_)

  "GitPython is a python library used to interact with git repositories, high-level like git-porcelain, or low-level like git-plumbing."

.. _git documentation: https://git-scm.com/doc
.. _git source code: https://github.com/git/git
.. _Dulwich documentation: https://www.dulwich.io/
.. _Dulwich source code: https://github.com/dulwich/dulwich
.. _GitPython documentation: http://gitpython.readthedocs.io/
.. _GitPython source code: https://github.com/gitpython-developers/GitPython
.. _GitPython known limitations: https://gitpython.readthedocs.io/en/stable/intro.html#limitations

`GitPython` is used to implement `git` based file scope change detection.

Semantic diff
-------------

Initially it was planned to use packages which provides "semantic diff" capabilities.
In comparison to a "file scope diff" a "semantic diff" contains contextual information
about the changes of source code files (instead of types of file states and line based differences).

In case of a Python language aware semanitc diff: Instead of beeing able to work with
the diff information "file xxx and file yyy was modified" one could work with information like
"in file xxx class a method b was modified and module scope function c was moved to file yyy".
This would allow to improve the granularity of the *impact map* and *coverage map* significantly.
Sadly at time of writing no packages are known which provide the required functionality
(reliability, completeness w.r.t. Python language entities) be used for semantic diffs.

The following alternatives have been evaluated to implement granular, semantic *determination of (file) changes* below the file level with semantic diffs.
However no alternative is usable and has not been evaluated in more detail.

- `Semantic Diff`_ is highly experimental and doesn't support Python 3.
- `SemanticMerge`_ is commercial and doesn't support Python 3.
- `Smart Differencer`_ is commercial and doesn't support Python 3.

.. _Semantic Diff: https://github.com/hoelzro/semantic-diff
.. _SemanticMerge: https://www.semanticmerge.com
.. _Smart Differencer: http://www.semanticdesigns.com/Products/SmartDifferencer/index.html

Continuous Integration environment
----------------------------------

Task execution
..............

`tox` is used to allow the execution of every CI job in various Python virtual environments.

Testing
.......

Tests of `python-tia` depend on the test runner `pytest (docs)`.
Execution of tests will be integrated into the CI environment via
`tox` environment `tests`.

.. _pytest (docs): https://docs.pytest.org

Static analysis
...............

Various static analyzers are integrated into the CI environment and
are invoked using various `tox` environments defined in `tox.ini`.
