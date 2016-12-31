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

import os
import time

from scriptbase import console
from scriptbase.cli import Boolean, String

from ..batch import TzarBatch


# Common command line options and arguments for archiving
ARCHIVE_CLI_ARGUMENTS = [
    Boolean('delete', 'delete files after archiving', '-d', '--delete', default=False),
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


def args_to_kwargs(command_args):
    return dict(
        dryrun=command_args.dryrun,
        pause=command_args.pause,
        verbose=command_args.verbose,
        delete=command_args.delete,
        ignoreobj=command_args.ignoreobj,
        ignorevcs=command_args.ignorevcs,
        noprogress=command_args.noprogress,
        outputdir=command_args.outputdir
    )


class BaseItem(object):

    def __init__(self, path, config_data,
                 dryrun=False,
                 pause=False,
                 verbose=False,
                 delete=False,
                 excludes=[],
                 ignoreobj=False,
                 ignorevcs=False,
                 noprogress=False,
                 outputdir=None):
        self.path        = os.path.normpath(path)
        self.config_data = config_data
        self.dryrun      = dryrun
        self.pause       = pause
        self.verbose     = verbose
        self.delete      = delete
        self.excludes    = excludes
        self.ignoreobj   = ignoreobj
        self.ignorevcs   = ignorevcs
        self.outputdir   = outputdir if outputdir else self.config_data.OUTPUT_DIRECTORY
        self.timestamp   = time.strftime('%y%m%d-%H%M%S')
        self.name        = '%s-%s' % (self.path.replace('/', '_'), self.timestamp)
        self.archive     = os.path.join(self.outputdir, self.name)
        self.compression = None
        self.noprogress  = noprogress
        self.batch       = TzarBatch(self, self.config_data.BINARY_PATTERNS,
                                     self.config_data.VCS_DIRECTORIES)
        if self.config_data.EXCLUDE_BINARIES:
            self.ignoreobj = True
        if self.config_data.EXCLUDE_VCS:
            self.ignorevcs = True
        self.excludes.extend(self.config_data.EXCLUDE_OTHER_PATTERNS)

    def check_output_directory(self):
        if not os.path.isdir(self.outputdir):
            if os.path.exists(self.outputdir):
                console.abort('"%s" exists and is not a directory' % self.outputdir)
            console.info('Creating %s...' % self.outputdir)
            try:
                os.mkdir(self.outputdir)
            except (IOError, OSError) as e:
                console.abort('Unable to create output directory', self.outputdir, e)

    def compare(self, runner):
        return self._perform(runner, 'compare')

    def create(self, runner):
        return self._perform(runner, 'create')

    def restore(self, runner):
        return self._perform(runner, 'restore')

    def is_metered(self):
        return self.batch.is_metered()

    def _perform(self, runner, name):
        self.outputdir = runner.expand(self.outputdir)
        self.archive = runner.expand(self.archive)
        self.check_output_directory()
        perform_method = getattr(self, 'build_%s_batch' % name)
        if not perform_method:
            console.abort('%s has no "%s" method.' % (self.__class__.__name__, name))
        perform_method(self.batch)
        return self.batch.run()
