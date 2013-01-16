class Test(object):
    def __init__(self, name, colorizer, text):
        self.name = name
        self.colorizer = colorizer
        self.text = text

class TestReader(object):
    def __init__(self, name, text):
        self.name = name
        self.text = text
    def __iter__(self):
        for line in self.text.split('\n'):
            yield line

test_data = [
    Test('ant', 'ant', '''\
compile:
   [depend] Deleted 17 out of date files in 0 seconds
   [delete] Deleting: src/whatever.h
    [javac] src/build.xml:28: warning: 'includeantruntime' was not set
    [javac] Compiling 13 source files to obj

licensecheck:
     [exec] SUCCESS. Found 0 license text errors, 0 files containing tabs or trailing whitespace.

ccompile:
     [exec]      [exec] make: Nothing to be done for `main'.
     [exec]      [exec] c++  -Wall xxx.cpp
     [exec]      [exec] clang: warning: argument unused during compilation: '-rdynamic'
     [exec]      [exec] LoggingTest:
     [exec]      [exec] 	TestManagerSetLevels: PASSED.
     [exec]      [exec] 	TestLoggerUsesProxyLevels: FAILED.
     [exec]      [exec] FAILED
     [exec]      [exec] IndexKeyTest:
     [exec]      [exec] 	Int64KeyTest: PASSED.
     [exec]      [exec] PASSED
     [exec]      [exec] ===============================================================================
     [exec]      [exec] TESTING COMPLETE (PASSED: 1, FAILED: 1)
     [exec]      [exec] *** FAILURE ***
     [exec]      [exec] ===============================================================================
     [exec]
     [exec] junit:
     [exec]     [junit] Tests run:   4, Failures:   0, Errors:   0, Time elapsed: 5.66 sec
     [exec]     [junit] Running org.voltdb.TestRestoreAgent
     [exec]     [junit] Tests run:  21, Failures:   0, Errors:   0, Time elapsed: 34.01 sec
     [exec]     [junit] Running org.voltdb.TestVoltDB
     [exec]     [junit]     testConfigurationValidate failed an assertion.
     [exec]     [junit]         org.voltdb.TestVoltDB(TestVoltDB.java:115)
     [exec]     [junit] Tests run:   4, Failures:   1, Errors:   0, Time elapsed: 3.92 sec
     [exec]     [junit] Test org.voltdb.TestVoltDB FAILED
     [exec]     [junit] Running org.voltdb.jdbc.TestJDBCDriver
     [exec]     [junit] Tests run:  17, Failures:   0, Errors:   0, Time elapsed: 3.32 sec
     [exec]
     [exec] BUILD FAILED
     [exec] /Users/scooper/workspace/voltdb/build.xml:1241: JUnit had failures
     [exec]
     [exec] Total time: 50 minutes 39 seconds
'''),
]
