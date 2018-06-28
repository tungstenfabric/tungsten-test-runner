# Contrail Unified Test Runner

Create a unified test runner that can run tests in parallel, handle flakiness
and create reports.

## Problem Description

Current test handling has a number of deficiencies:

  - No common support for running tests in parallel
  - No way to gauge current progress
  - Very verbose output to console
  - Lack of robust test flakiness support
  
All those points slow down development - the full test suite (scons `test`
target) require over 7 hours to run, with a high probability of failure due
to the test flakiness. Furthermore, our current flakiness factor for unittest
jobs running in CI is estimated at over 20%, requiring a constant baby sitting
of CI jobs to ensure that they pass.

## Proposed Change

This spec proposes a new test runner thar provides a unified way to gather
and run a list of tests based on the review, with the following
improvements:

  - Running tests concurrently in an isolated environment

  - Cleaner console output, printing the name of the ran test and its status.

  - Unified test reports for the entire project - both human readable HTML,
    as well as machine-parseable XML reports.
 
  - Handling test flakiness, both by providing a way to rerun failed tests
    as well as denoting tests, specifying conditions when the test should
    fail the job.
    
  - Gathering and processing core files for tests, giving developers
    additional tools to debug test failures in CI.
    
### Test Layout

To support listed functionality, this proposal deprecates a SCons-based
test runner, and the existing `ci_unittests.json` file used by our CI
to build a relation between tests. SCons is relegated to the process
of building binary tests, as well as building sdist tarballs for python
packages. In place of `ci_unittests.json` we introduce `tests.yaml` layout
that describes each Contrail component (e.g. _controller_, _config_,
_agent_) and a list of modules (e.g. _api-server_, _bgp_, _bfd_).

#### tests.yaml

Test runner looks for the tests.yaml file in the root directory of each
of our projects (e.g. _controller_, _analytics_, _vrouter_). Those files
are then parsed and merged into a single test layout. This helps us with
our repository split efforts, by making it easier to modify tests and
mappings in a single review.

The proposed layout of the `tests.yaml` file can be seen below:

```yaml
- module:
    # the name of the module being tested - has to be unique across all
    # projects
    name: bfd
    # a component this module is a part of - all modules that are part of
    # the component will be run when one of them changes.
    component: control
    scons:
      # a list of SCons targets to run before we execute tests.
      targets:
        - controller/src/bfd:test
        - controller/src/bfd/rest_api:test
    driver:
      # python module used to execute tests - this allows us not only
      # supporting various types of source projects - Python, C++, Go
      # but also an easy way of creating more specific test runners, e.g.
      # IsolatedGTestRunner that uses system-level sandbox to isolate
      # test network and filesystem.
      gtest:
        # Whether tests for this module can be safely executed in parallel.
        # Test scheduler will group tests into those that can, and run them
        # all in parallel, and then will run all tests that are unsafe in
        # sequence.
        parallel: False
        # For GoogleTest-based tests, a list binaries to execute is provided.
        test_suites:
          - ^bfd/tests/.*_test$
          - ^bfd/rest_api/tests/.*_test$
        # Test overrides
        test_overrides:
          # This override skips execution of all the binaries listed. This
          # list can be either a string or a regular expression.
          - file_matchers:
              - ^bfd/rest_api/bfd_config_test$
            disabled: True
          # This override specifies that tests from the `bfd_session_test`
          # test suite matching the specified regular expression should
          # be considered flaky, with the execution strategy of `Pass3of5`
          # meaning that the test will be executed 5 times, and considered
          # to be passing only when 3 of those runs succeed.
          - file_matchers:
              - ^bfd/test/bfd_session_test$
            test_matchers:
              - ^.*PollSendTest$
            flaky:
              strategy: Pass3of5
```

Each module gets its own test entry - each entry shares a set of data (module
name, its component, SCons targets to execute), as well as the description
of how tests should be executed - the TestRunner module, per-test overrides
(disabling tests, strategies how to handle flakiness).

### User Interface

`tntestr` script is the main entry point of the test runner. It can be used
to run both the entire test collection, as well as test suites for specific
modules, and even single test cases.

Behind scenes, it interacts with our SCons build system to build all the
required dependencies, handles test scheduling and test retrying as well
as the processing of coredumps, and generates the final report for the user.

### SCons interactions

Test Running functionality of SCons is removed, and it's delegate to the
process of building tests - compiling binaries and creating sdist tarballs,
as well as resolving source-level dependencies.

This solves the current deficiency where test build-time errors can shadow
test failures. Parallel test building is also greatly simplified, as there
is no longer need to make sure that tests are executed in sequence after
the build finishes.

#### Two-way verification of mappings

One of the problems with the current `ci_unittests.json` approach is the
possibility of mappings between that file and our SCons scripts diverging.
That's due to the fact that there is no mechanism to verify that they always
stay in sync. In the worst-case scenario that can introduce delayed failures,
when the SCons target was deleted, or broken in some way, but it wasn't executed
as part of the review being merged - any consecutive review can fail afterwards,
if it tries to build that target. This adds to the flakiness of the entire CI.

This spec adds a way to list all test targets from SCons, and match them with
the content of the `tests.yaml` files - any discrepancies lead to an early error
in the CI.

To support that, we add `--list-tests` command line options to our SCons, which
will output jsonlines[1] stream with the list of all the testsuites known
to our build system. We achieve that by extending the existing SCons builders
used for tests, to add a marker indicating that the target is a test.

[1]: http://jsonlines.org

### Test Scheduling

To speed up test execution, tests are executed in parallel. Test Scheduler
component is responsible for handling a queue of tests and scheduling them
based on the various conditions.

It also handles console output from tests, saving them to files, as well
as multiplexing stdout to print progress to the user.

By default all tests coming from the same testsuite (python package,
gtest binary) are run sequentially, but that can be changed on the per-module
level.

### Test Retrying

To limit a number of false negatives, test runner retries tests explicitly
marked as flaky a set number of times, and then marks test as succeded/failed
based on the number of passing retries.

Requiring tests to be marked as flaky is done to keep the overall quality
of tests as high as possible - marking each test as flaky is a conscious
decision made by developers. 

#### Flakiness Strategies

Test Runner will provide a set number of strategies to use for retrying flaky
tests, starting with `Pass2of3` and `Pass3of5`. While adding additional
strategies should be discussed, a more generic way of defining what
constitutes a passing flaky test is discouraged - this could lead
to nonoptimal strategies being selected e.g. passing a test as long as
a single run succeeded. 

### CoreDump Processing

To provide developers with more tools for debugging their code, especially
in CI, test runner gathers backtrace for binaries that have crashed - the
backtrace is then uploaded to the logserver along with other test artifacts,
and can be evaluated by the developer.

### Results Reporting

[TODO]

#### Console output

[TODO]

#### XML and HTML reports

[TODO]

### Language and Framework Support

All languages used within _Contrail VNC_[1] must be supported out of the box,
with support for additional languages being left for later time.

[1]: Contrail VNC in this context means a set of projects that are currently
     being built together using our SCons system.

#### Python

All python components shall be rewritten to utilize tox for executing both
tests, as well as various linters (e.g. pep8, bandit, pylint). This provides
us with a unified interface for executing tests, simplifying design of the
test runner itself.

#### C++

All Google Test-based tests have checked for supporting standard gtest
commandline arguments (e.g. `--gtest_list_tests`, `--gtest_filter`) and
non-conforming tests shall be fixed.

#### C

Any C based tests have to be checked for providing a way to generate a list
of tests, execution-time filtering, and generating common XML reports (jUnit
XML).

#### Go

[TODO]

## CI Impact

If the runner is working properly, it should cut down the time required
to run our tests, as well as lower an amount of false negatives with
an improved flaky tests handling.

This spec also opens a way to introduce long-term test statistics, making
it possible to keep track of trends as well as catch new flaky test
occurrences much sooner in the development process. 

## User Impact

This spec introduces a new tool that has to be installed by all developers
who want to work on OpenContrail. Even though we take care to keep supporting
some existng workloads (like keeping the ability to run python and C++ tests
manually by executing the `tox` test runner, and gtest binaries directly) the
SCons-based testing will no longer be possible.

Test Runner will be distributed through https://pypi.python.org/ and will run
on Ubuntu 16.10+, CentOS/RHEL 7.4+ (with EPEL repositories) and any other
distribution that has access to Python 3.6.3+ (this includes Ubuntu 16.04,
for which we'll backport python3.6 and related packages).

To help developers transition to the new test execution model, all existing
`:test` targets will print the instructions on how to execute tests using
contrail test runner and return with error code 1 to indicate that no tests
were executed.

## Implementation

A proof-of-concept can currently be found on GitHub[3].

[3]: https://github.com/kklimonda/contrail-test-runner.

## History

| Version | Author                                     | Remarks         |
| ------: | -----------------------------------------: | --------------: |
| 0.1     | Krzysztof Klimonda <kklimonda@juniper.net> | Initial version |
