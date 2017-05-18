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

"""Base class for archive items."""

import os
import time

#pylint: disable=import-error
from scriptbase import console
from scriptbase.cli import Boolean, String
from scriptbase.utility import DictObject

from ..batch import TzarBatch


# Common command line options and arguments for archiving
ARCHIVE_CLI_ARGUMENTS = [
    Boolean('delete', 'delete source files after archiving', '-d', '--delete', default=False),
    Boolean('ignoreobj', 'ignore binary files '
                         '(affected by the BINARY_PATTERNS configuration option)',
            '--ignore-obj', default=False),
    Boolean('ignorevcs', 'ignore source control subdirectories '
                         '(affected by the VCS_DIRECTORIES configuration option)',
            '--ignore-vcs', default=False),
    Boolean('noprogress', 'disable progress meter', '--no-progress', default=False),
    String('outputdir', 'output directory', '-o', '--output-dir'),
    String('path', 'path(s) to archive', nargs='+'),
]

OPTIONS = dict(
    dry_run=False,
    pause=False,
    verbose=False,
    delete=False,
    excludes=[],
    ignoreobj=False,
    ignorevcs=False,
    noprogress=False,
    outputdir=None,
)


def option_attributes_to_dictionary(option_attributes, **additional_symbols):
    """Convert options as attributes to a dictionary."""
    option_dictionary = {}
    for keyword, default_value in OPTIONS.items():
        if hasattr(option_attributes, keyword):
            option_dictionary[keyword] = getattr(option_attributes, keyword)
        else:
            option_dictionary[keyword] = default_value
    option_dictionary.update(additional_symbols)
    return option_dictionary


def option_dictionary_to_attributes(option_dictionary):
    """Convert options as a dictionary to attributes."""
    option_attributes = DictObject()
    bad_keywords = sorted(list(set(option_dictionary.keys()).difference(OPTIONS.keys())))
    if bad_keywords:
        plural = 's' if len(bad_keywords) > 1 else ''
        console.abort('Unexpected option keyword%s: %s' % (plural, ' '.join(bad_keywords)))
    for keyword in option_dictionary:
        if keyword in OPTIONS:
            setattr(option_attributes, keyword, option_dictionary.get(keyword))
        else:
            bad_keywords.append(keyword)
    return option_attributes


class BaseItem(object):
    """Base class for archive items."""

    def __init__(self, path, config_data, **option_dictionary):
        """Base archive item constructor."""
        self.path = os.path.normpath(path)
        self.config_data = config_data
        self.options = option_dictionary_to_attributes(option_dictionary)
        if not self.options.outputdir:
            self.options.outputdir = self.config_data.OUTPUT_DIRECTORY
        if self.config_data.EXCLUDE_BINARIES:
            self.options.ignoreobj = True
        if self.config_data.EXCLUDE_VCS:
            self.options.ignorevcs = True
        self.options.excludes.extend(self.config_data.EXCLUDE_OTHER_PATTERNS)
        name = '%s-%s' % (self.path.replace('/', '_'), time.strftime('%y%m%d-%H%M%S'))
        self.archive = os.path.join(self.options.outputdir, name)
        self.batch = TzarBatch(self,
                               self.config_data.BINARY_PATTERNS,
                               self.config_data.VCS_DIRECTORIES)

    def check_output_directory(self):
        """Make sure there's a good output directory."""
        if not os.path.isdir(self.options.outputdir):
            if os.path.exists(self.options.outputdir):
                console.abort('Output directory exists and is not a directory: %s'
                              % self.options.outputdir)
            console.info('Creating output directory: %s' % self.options.outputdir)
            try:
                os.mkdir(self.options.outputdir)
            except (IOError, OSError) as exc:
                console.abort('Unable to create output directory', self.options.outputdir, exc)

    def compare(self, runner):
        """Invoke the compare function."""
        return self._perform(runner, 'compare')

    def create(self, runner):
        """Invoke the create function."""
        return self._perform(runner, 'create')

    def restore(self, runner):
        """Invoke the restore function."""
        return self._perform(runner, 'restore')

    def is_metered(self):
        """Return true if progress is metered."""
        return self.batch.is_metered()

    def _perform(self, runner, name):
        self.options.outputdir = runner.expand(self.options.outputdir)
        self.archive = runner.expand(self.archive)
        self.check_output_directory()
        perform_method = getattr(self, 'build_%s_batch' % name)
        if not perform_method:
            console.abort('%s has no "%s" method.' % (self.__class__.__name__, name))
        perform_method(self.batch)
        return self.batch.run()
