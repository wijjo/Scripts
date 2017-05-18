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

"""Command Batch class extended for Tzar."""

import sys

#pylint: disable=import-error
from scriptbase import command
from scriptbase import shell


class TzarBatch(command.Batch):
    """Command batch for Tzar."""

    copy_command = 'cp -Rpv' if sys.platform in ['darwin'] else 'cp -av'

    # Display progress with "pv", if available.
    pv_path = shell.find_executable('pv')

    def __init__(self, item, binary_patterns, vcs_directories):
        """Construct batch with item to archive and filtering info."""
        self.item = item
        self.binary_patterns = binary_patterns
        self.vcs_directories = vcs_directories
        command.Batch.__init__(self, dry_run=item.options.DRY_RUN)

    def add_exclude_args(self, option):
        """Add exclusion arguments."""
        def _add_excludes(excludes, test=None, leader='', trailer=''):
            if test is None or test:
                for exclude in excludes:
                    # Don't separate by whitespace when the option ends with '=' or '!', e.g. P7Zip.
                    if option[-1] in ('!', '='):
                        self.add_args((option, leader, exclude, trailer))
                    else:
                        self.add_args(option, (leader, exclude, trailer))
        _add_excludes(self.binary_patterns, test=self.item.options.ignoreobj)
        _add_excludes(self.vcs_directories, test=self.item.options.ignorevcs,
                      leader='*/', trailer='/*')
        _add_excludes(self.item.options.excludes)

    def is_metered(self):
        """Return True if progress is metered."""
        return self.pv_path and not self.item.options.noprogress

    def add_metered_redirection_args(self, output_path, path):
        """Add command arguments to meter progress with pv."""
        self.add_args('-', path)
        self.add_operator('|')
        self.add_args(self.pv_path, '-rbt')
        self.add_operator('>')
        self.add_args(output_path)

    def add_move_command(self, src, dst):
        """Add command to move a file or directory."""
        self.add_command('mv', '-v', src, dst)

    def add_copy_command(self, src, dst):
        """Add command to copy a file or directory."""
        self.add_command(self.copy_command, src, dst)

    def add_archive_copy_move_command(self):
        """Add command to copy or move the archive."""
        if self.item.options.delete:
            self.add_move_command(self.item.path, self.item.archive)
        else:
            self.add_copy_command(self.item.path, self.item.archive)

    def add_compression_command(self, path):
        """Add command to perform commpression."""
        self.add_command(self.item.options.compression, path)

    def add_archive_compression_command(self):
        """Add command to compress the archive."""
        self.add_compression_command(self.item.archive)

    def add_source_deletion(self):
        """Add command as needed to delete the source."""
        if self.item.options.delete:
            self.add_command('rm', '-rvf', self.item.path)
