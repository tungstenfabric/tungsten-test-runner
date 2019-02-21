# TungstenFabric Unit Tests Runner

## TestRunner

The new [testrunner](<https://github.com/tungstenfabric/tungsten-test-runner>)
has been developed to overcome the shortcomings of the former test runner,
which was a complicated [shell](<https://github.com/Juniper/contrail-test/blob/master/testrunner.sh>)
script, mainly but not limited to:

* the ability to rerun failed test cases - to mitigate test flakiness (implemented)
* the ability to run tests in parallel (not implemented)

TestRunner internally uses scons to run the tests. The input to TestRunner
is a list of test targets to run, the same ones which are passed to scons.

After running scons, TestRunner analyzes the output [XML report files](#XML-report-file)
and determines whether any test target needs to be rerun. Current implementation
reruns whole test targets although it should be possible to implement
rerunning single test cases (both for C++ and Python tests).

### Establishing Test Targets To Run

The [contrail-gather-unittest.rb](https://github.com/Juniper/contrail-zuul-jobs/blob/master/roles/contrail-unittests-tntestr/files/contrail-unittests-gather.rb)
script is used to determine which scons test targets should be run based on
the changes in the changeset. The [ci_unittest.json](#ci-unittest.json)
file is used for this.

### ci-unittest.json

This json file maps contrail modules (e.g. contrail-libs) and the modules
source directories to test targets that should be run. If a change in the
changeset matches any source directory on the list of source directories, all
test targets from the list are added to the runtime list.

There is an abstract module named 'default' defined, test targets from which will
be run if no module/source directory pair will match any of the changes
in the changeset. This 'default' module contains most test targets defined across
TungstenFabric project. Should a new test target be defined and would
needed to be run as default it should be added to the list of test targets
under 'default' key.

### XML report file

The following scons command will output the paths of the XML and log files
where TestRunner will expect them to be available after tests are run:


```bash
    scons -Q --warn=no-all --describe-tests
```

Passing a specific test target is also possible e.g.

```bash
    scons -Q --warn=no-all --describe-tests controller/src/config/api-server:test
```

Example output would be:

```
{
    "log_path": "/home/zuul/contrail-5.1.0/build/debug/config/api-server/test.log",
    "matched": true,
    "xml_path": "/home/zuul/contrail-5.1.0/build/debug/config/api-server/test-results.xml",
    "node_path": "/home/zuul/contrail-5.1.0/build/debug/config/api-server/test.log"
}
```

#### Format

TestRunner expects the XML reports to be of the Junit XML format an example
of which is presented below:

```bash
<?xml version="1.0" encoding="UTF-8"?>
<testsuites disabled="" errors="" failures="" name="" tests="" time="">
    <testsuite disabled="" errors="" failures="" hostname="" id=""
               name="" package="" skipped="" tests="" time="" timestamp="">
        <properties>
            <property name="" value=""/>
        </properties>
        <testcase assertions="" classname="" name="" status="" time="">
            <skipped/>
            <error type=""/>
            <failure type=""/>
            <system-out/>
            <system-err/>
        </testcase>
        <system-out/>
        <system-err/>
    </testsuite>
</testsuites>
```

Note:
* there can only be one `testsuites` element
* there can be multiple `testsuite` elements
* a `testsuite` element may contain multiple `testcase` elements
* the `properties` element of the `testsuite` element may be skipped
* the nested elements of `testcase` may be skipped
* `system-out` and `system-err` of `testsuite` element may be skipped
* the text of `failure` element should contain the error log from the failed
  test case

The XML reports are also used for gathering unit test statistics
(see: [statistics gathering script](https://github.com/tungsten-infra/ci-utils/tree/master/tungsten_ci_utils/test_statistics),
[Grafana](http://148.251.5.91/grafana/dashboard/db/test-statistics?orgId=1)).

### SCons Builders

There are two important scons builders defined in [rules.py](https://github.com/Juniper/contrail-build/blob/master/rules.py)
file. These are:

* TestSuite(...)
* SetupPyTestSuite(...)

Using these builders ensures the `--describe-tests` scons method will
return proper log and XML report paths.

The TestSuite(...) builder should be used for C++ modules,
SetupPyTestSuite(...) for python modules.

There is a second Python builder called SetupPyTestSuiteWithDeps. Use
it only when SetupPyTestSuite does not fulfill your needs.

TestSuite(...), when called, configures the runtime environment with the
GTEST_OUTPUT variable, setting the XML report path, thus no further
configuration is needed.

When using SetupPyTestSuite it is expected that:

* the output log file is named 'test.log'
* the output XML report file is named 'test-results.xml'

### Example Contrail module configurations

There are a number of modules which already are configured correctly and
output the expected XML reports.

#### api-server module

The api-server module uses [SetupPyTestSuite(...)](https://github.com/Juniper/contrail-controller/blob/master/src/config/api-server/SConscript#L64)
builder. This ensures XML report paths will be known
to TestRunner.

The module also uses tox to run the tests and
[subunit2junitxml]((https://github.com/Juniper/contrail-controller/blob/master/src/config/api-server/tox.ini#L28))
to produce the XML report.

#### api-lib module

The api-lib module configuration is similar to api-server. The difference
is it uses [SetupPytestSuiteWithDeps](https://github.com/Juniper/contrail-api-client/blob/master/api-lib/SConscript#L112)
directly.

#### bgp module

The bgp module uses [TestSuite](https://github.com/Juniper/contrail-controller/blob/master/src/bgp/test/SConscript#L769)
builder. The builder assumes [Google Test](https://github.com/google/googletest)
is used as the testing framework.

### Summary

In order for the TestRunner to be able to analyze the results from the
tests and rerun them in case of flakiness you should:

* for Python use either SetupPyTestSuite (or SetupPyTestSuiteWithDeps) builder
  and make sure the tests produce XML reports in the expected format
* for C++ use TestSuite builder and make sure the tests produce XML
  reports in the expected format (Google Test does this out of the box)
* if you're adding a new test target consider whether it should be added
  to the 'default' in [ci_unittest.json](#ci-unittest.json) file

