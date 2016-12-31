# Copyright 2016 Steven Cooper
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

# TZAR - simple archiving front end
#
# Features:
#
#   Multiple archive formats:
#
#     - gzip    standard with high speed and less compression
#     - bzip2   standard with better compression than gzip, but slower
#     - xz      newer standard with better compression than bzip2, but slower
#     - zip     multi-platform format with good speed/compression balance
#     - p7zip   slower high compression format
#     - lzip    another slower high compression format
#     - put     straight file copy
#
#   Performance:
#
#     Performance is determined by the external command line tool that is used
#     for a particular format, but it takes advantage of faster multi-threaded
#     archiving tools like pigz, pxz, lbzip2, and pbzip2 when available.
#
#   Operations:
#
#     - compress using format choice
#     - compare to archive (limited)
#     - restore from archive (limited)
#     - generate a configuration file template
#
#   Usability:
#
#     - Provides a simple command line interface, e.g. that allows creating an
#       archive without specifying an output file.
#     - Uses pv when it is available to display a real-time i/o progress meter.
#     - Supports per-location and global configuration files to fine-tune
#       default options for different directories, e.g. to always exclude local
#       temporary files from the archive.

from glob import glob

from scriptbase.command import BatchError, BatchFailure
from scriptbase.shell import find_executable
from scriptbase.cli import Main, main, Command, Boolean, String
from scriptbase.console import abort, set_verbose
from scriptbase.configuration import ConfigSpec, Config


CFG_SPECS = [
    ConfigSpec(
        'BINARY_PATTERNS',
        [
            '*.o',
            '*.so',
            '*.so.*',
            '*.co',
            '*.pyc',
            '*.pyd',
            '*.Plo',
            '*.la',
            '*.lai',
            '*.lo',
            '*.a',
            '*.dll',
            '*.DLL',
            '*.exe',
            '*.EXE',
            '*.lib',
            '*.LIB',
            '*.dylib',
            '*.jnilib',
            '*.jar',
            '*.deb',
            '*.rpm',
            '*.zip',
            '*.ZIP',
            '*.gz',
            '*.tgz',
            '*.bz2',
            '*.xz',
            '*.lz',
            '*.sym',
            '*.bin',
            '*/tags',
        ],
        'Binary file wildcard patterns that are optionally ignored.'
    ),
    ConfigSpec(
        'EXCLUDE_BINARIES',
        False,
        'Exclude binary files if True.'
    ),
    ConfigSpec(
        'EXCLUDE_OTHER_PATTERNS',
        [],
        'Wildcard patterns for other excluded files.'
    ),
    ConfigSpec(
        'EXCLUDE_VCS',
        False,
        'Exclude VCS directories if True.'
    ),
    ConfigSpec(
        'OUTPUT_DIRECTORY',
        '.%(program_name)s',
        'Output subdirectory name.'
    ),
    ConfigSpec(
        'REPLACEMENT_GZIP',
        find_executable('pigz'),
        'Compatible gzip replacement. By default pigz is used when available.'
    ),
    ConfigSpec(
        'REPLACEMENT_BZIP2',
        find_executable('pbzip2', 'lbzip2'),
        'Compatible bzip2 replacement. By default pbzip2 or lbzip2 are used when available.'
    ),
    ConfigSpec(
        'REPLACEMENT_XZ',
        find_executable('xz'),
        'Use xz as an external program to benefit from its multi-threading.'
    ),
    ConfigSpec(
        'REPLACEMENT_LZIP',
        find_executable('plzip'),
        'Compatible lzip replacement. By default plzip is used when available.'
    ),
    ConfigSpec(
        'VCS_DIRECTORIES',
        [ '.svn', '.cvs', '.git' ],
        'VCS directory names that are optionally ignored.'
    ),
]

@Main(
    description='Simple backup archiver.',
    configuration=CFG_SPECS,
    support_verbose=True,
    support_dryrun=True,
    support_pause=True,
    support_discovery=True,
)
def _(runner):
    pass
