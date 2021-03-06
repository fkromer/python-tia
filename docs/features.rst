.. _features:

Features
========

- **Change detection**: `tia` determines changes to the production and test code which is under version control.
- **Semantic mapping**: `tia` understands mappings of directories and files to test and analysis command line applications in a *semantic map* as *pipelines*.
- **Pipeline execution**: `tia` executes *pipelines* defined in the *semantic map*.
- **Coverage mapping**: `tia` traces which production code is executed by every single test via dynamic analysis and keeps track of it in a *coverage map* (test code vs. production code).
- **Impact mapping**: `tia` determines which test code needs to be executed in case of production code changes and keeps track of it in a *impact map* (production code vs. test code).