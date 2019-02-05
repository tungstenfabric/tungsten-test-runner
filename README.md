# [DRAFT] TungstenFabric Unit Tests Runner

## TestRunner

This section should describe how the new testrunner works (in general).
Mention that:

* it runs scons underneath
* it has the ability to rerun failed test targets based on output xml files from
  the tests, thus the tests need to output xml files of given format (describe the format in
  a separate section)
* where the xml files need to be available after running the tests in order for the test runner
  to pick them up
* it has (probably not implemented yet) the ability to run tests in parallel, but needs additional
  configuration in order to do so (consult the documentation of the test runner for specifics;
  create JIRA tasks for implementation if needed)
* mention ci_unittests.json and the main SConscript file + the main test alias; explain the format/logic
  of the json file
* module's scons test aliases need to be added to the 'default' test target in ci_unittest.json in order for them
  to be run when no test target is specified
* mention (or maybe not?) the contrail-gather-unittest.rb file which determines which unit test
  targets should be run based on the changesets (also make sure that the script considers the dependent
  reviews while at it)
* the new testrunner job runs test targets one by one so it is easily verifiable whether a newly
  added test target has been run

### XML report file

Describe the format of the report file which should be generated after running the test target
(/test suites).

Give examples of contrail modules which already generate such XML's. Point to the configuration.
There should be at least two python modules with some tox configuration, executed from a SConscript.
There PROBABLY is a c++ module with gTest configuration which also outputs such a report file).

### Contribution

Summarise what will probably written in previous sections. Something of the following sort:

'In order for the new testrunner to be able to analyze and rerun your tests you should:

* for Python configure XXXX
* for C++ configure YYY'

