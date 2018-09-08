.. _reasoning:

Reasons for python-tia
======================

- **"As a developer I want to call tia that the recently changed tests on my dev machine are selected for execution."**
  Triggering test execution in a Test Driven Development (TDD) manner on a developer machine may be annoying because tests need to be selected explicitly for execution.
  When executing all tests the execution time may be that long that it prevents from adapting an effective Test Driven Development (TDD) workflow.
- **"As a developer I want to call tia that the tests are selected for execution which correspond to the recently changed production code on my dev machine."**
  It may not be obvious what tests need to be executed after production code was changed.
  When executing all tests the execution time may be that long that it prevents from adapting an effective Test Driven Development (TDD) workflow.
- **"As a developer I want to call tia that the recently changed production code on my dev machine is selected for static analysis."**
  Running analyzers in a Test Driven Development (TDD) manner may be annoying because it's not always obvious if they need to be run at all and in case they should over which files they should run.
  Running analyzers over more files than required is (usually not critical but anyway) a waste of time.
