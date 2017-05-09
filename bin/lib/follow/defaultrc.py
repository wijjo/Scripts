# Copyright 2016-17 Steven Cooper
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Default rc file for follow."""

#pylint: disable=invalid-name
default_rc_text = r'''
{
    "colorizers": [
        {
            "names": [
                "java"
            ],
            "scanners": [
                {
                    "pattern": "(\\[INFO\\])",
                    "style": "INFO"
                },
                {
                    "pattern": "(\\[WARN\\])",
                    "style": "WARNING"
                },
                {
                    "pattern": "(\\[ERROR\\])",
                    "style": "ERROR"
                },
                {
                    "pattern": "\\[java\\][ \t]*([a-zA-Z.]*Exception):",
                    "style": "ERROR"
                }
            ]
        },
        {
            "names": [
                "make",
                "gmake"
            ],
            "scanners": [
                {
                    "pattern": "^\\+ ([A-Z][A-Z_0-9]*=.*|shift|case.*|'\\['.*|)$",
                    "style": "HIDE"
                },
                {
                    "pattern": "^\\+ \\[.*\\]$",
                    "style": "HIDE"
                },
                {
                    "pattern": "^[+] exec ",
                    "style": "INFO"
                },
                {
                    "pattern": "[wW][aA][rR][nN][iI][nN][gG]:",
                    "style": "WARNING"
                },
                {
                    "pattern": "[eE][rR][rR][oO][rR]:",
                    "style": "ERROR"
                },
                {
                    "pattern": "[eE][rR][rR][oO][rR] *[0-9]+",
                    "style": "ERROR"
                },
                {
                    "pattern": "[fF][aA][tT][aA][lL] [eE][rR][rR][oO][rR]",
                    "style": "ERROR"
                },
                {
                    "pattern": "[eE][rR][rR][oO][rR] [cC][oO][dD][eE]",
                    "style": "ERROR"
                },
                {
                    "pattern": "^\\s+(ar|ld|rm) ",
                    "style": "INFO"
                },
                {
                    "pattern": "^make(\\[\\d+\\])?:",
                    "style": "HEADING"
                }
            ]
        },
        {
            "names": [
                "ant"
            ],
            "scanners": [
                {
                    "pattern": "FAILED: [1-9]",
                    "style": "BAD"
                },
                {
                    "pattern": "PASSED: [1-9]",
                    "style": "GOOD"
                },
                {
                    "pattern": "[\\]:] FAILED",
                    "style": "BAD"
                },
                {
                    "pattern": "[\\]:] PASSED",
                    "style": "GOOD"
                },
                {
                    "pattern": "\\[exec\\] SUCCESS",
                    "style": "SUCCESS"
                },
                {
                    "pattern": "^[a-zA-Z0-9_\\- ]+[^: ]*:",
                    "style": "HEADING"
                },
                {
                    "pattern": "\\[junit\\]   Running ",
                    "style": "HEADING"
                },
                {
                    "pattern": "[wW][aA][rR][nN][iI][nN][gG]:",
                    "style": "WARNING"
                },
                {
                    "pattern": "\\[WARNING\\]",
                    "style": "WARNING"
                },
                {
                    "pattern": "^[ ]+\\[javac\\][ ]+[^ ]+[.]java:[0-9]+:",
                    "style": "ERROR"
                },
                {
                    "pattern": "^[ ]+\\[java\\][ \ta-zA-Z0-9._]+Exception:",
                    "style": "ERROR"
                },
                {
                    "pattern": "^[ ]+\\[java\\][ \t]+Caused by:",
                    "style": "ERROR"
                },
                {
                    "pattern": "\\[ERROR\\]",
                    "style": "ERROR"
                },
                {
                    "pattern": "^[ ]+\\[exec\\][ ]+[^ ]+[.](cpp|cxx|c|h|hpp|hxx|o|so|a):[0-9]+:",
                    "style": "ERROR"
                },
                {
                    "pattern": "[eE][rR][rR][oO][rR]:",
                    "style": "ERROR"
                },
                {
                    "pattern": "[eE][rR][rR][oO][rR] *[0-9]+",
                    "style": "ERROR"
                },
                {
                    "pattern": "[fF][aA][tT][aA][lL] [eE][rR][rR][oO][rR]",
                    "style": "ERROR"
                },
                {
                    "pattern": "[eE][rR][rR][oO][rR] [cC][oO][dD][eE]",
                    "style": "ERROR"
                },
                {
                    "pattern": "returned [1-9][0-9]* exit",
                    "style": "ERROR"
                },
                {
                    "pattern": "BUILD SUCCESSFUL",
                    "style": "SUCCESS"
                },
                {
                    "pattern": "BUILD FAILED",
                    "style": "FAILURE"
                },
                {
                    "pattern": " ((Errors|Failures):\\s*[1-9][0-9]*)",
                    "style": "BAD"
                },
                {
                    "pattern": " FAILED",
                    "style": "BAD"
                },
                {
                    "pattern": " ((Errors|Failures):\\s*0)[^0-9]",
                    "style": "GOOD"
                },
                {
                    "pattern": " Testsuite\\:",
                    "style": "SECTION"
                },
                {
                    "pattern": "(\\[[^ ]*\\])",
                    "style": "INFO"
                }
            ]
        },
        {
            "names": [
                "log"
            ],
            "scanners": [
                {
                    "pattern": "WARN",
                    "style": "WARNING"
                },
                {
                    "pattern": "ERROR",
                    "style": "ERROR"
                },
                {
                    "pattern": "FATAL",
                    "style": "BAD"
                }
            ]
        },
        {
            "names": [
                "svn"
            ],
            "scanners": [
                {
                    "pattern": "U[ ]+",
                    "style": "INFO"
                },
                {
                    "pattern": "Updated to revision",
                    "style": "INFO"
                },
                {
                    "pattern": "At revision",
                    "style": "INFO"
                },
                {
                    "pattern": "A[ ]+",
                    "style": "HEADING"
                },
                {
                    "pattern": "C[ ]+",
                    "style": "ERROR"
                },
                {
                    "pattern": "G[ ]+",
                    "style": "SECTION"
                },
                {
                    "pattern": "D[ ]+",
                    "style": "WARNING"
                }
            ]
        }
    ],
    "styles": {
        "ADMIN": {
            "bg": 4,
            "bold": true,
            "fg": 7,
            "hide": false,
            "marker": null,
            "name": "Admin"
        },
        "BAD": {
            "bg": null,
            "bold": true,
            "fg": 1,
            "hide": false,
            "marker": null,
            "name": "Bad"
        },
        "DEBUG": {
            "bg": null,
            "bold": false,
            "fg": 4,
            "hide": false,
            "marker": null,
            "name": "Debug"
        },
        "DEFAULT": {
            "bg": null,
            "bold": false,
            "fg": 7,
            "hide": false,
            "marker": null,
            "name": "Default"
        },
        "ERROR": {
            "bg": null,
            "bold": true,
            "fg": 1,
            "hide": false,
            "marker": "ERROR",
            "name": "Error"
        },
        "FAILURE": {
            "bg": 1,
            "bold": true,
            "fg": 7,
            "hide": false,
            "marker": null,
            "name": "Failure"
        },
        "GOOD": {
            "bg": null,
            "bold": true,
            "fg": 5,
            "hide": false,
            "marker": null,
            "name": "Good"
        },
        "HEADING": {
            "bg": null,
            "bold": true,
            "fg": 6,
            "hide": false,
            "marker": null,
            "name": "Heading"
        },
        "HIDE": {
            "bg": null,
            "bold": false,
            "fg": null,
            "hide": true,
            "marker": null,
            "name": "Hide"
        },
        "INFO": {
            "bg": null,
            "bold": true,
            "fg": 2,
            "hide": false,
            "marker": null,
            "name": "Info"
        },
        "SECTION": {
            "bg": null,
            "bold": true,
            "fg": 5,
            "hide": false,
            "marker": null,
            "name": "Section"
        },
        "SUCCESS": {
            "bg": 2,
            "bold": true,
            "fg": 7,
            "hide": false,
            "marker": "FAILURE",
            "name": "Success"
        },
        "WARNING": {
            "bg": null,
            "bold": true,
            "fg": 3,
            "hide": false,
            "marker": null,
            "name": "Warning"
        }
    }
}
'''.strip()
