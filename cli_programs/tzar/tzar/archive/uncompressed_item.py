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

"""Uncompressed file or directory archive item."""

import os

#pylint: disable=import-error
from scriptbase import console
from scriptbase import disk

from .base_item import BaseItem

class UncompressedItem(BaseItem):
    """Uncompressed file or directory archive item."""

    @classmethod
    def item_for_path_if_matching(cls, path, parsed_name, config_data, **kwargs):   #pylint: disable=unused-argument
        """Create an archive item if the file or directory exists."""
        if os.path.exists(path):
            return UncompressedItem(path, config_data, **kwargs)

    def __init__(self, path, config_data, **kwargs):
        """Construct archive item."""
        BaseItem.__init__(self, path, config_data, **kwargs)

    def build_create_batch(self, batch):    #pylint: disable=no-self-use
        """Populate a command batch for creating the archive."""
        batch.add_archive_copy_move_command()

    def build_restore_batch(self, batch):
        """Populate a command batch for restoring the archive."""
        target = disk.get_versioned_path(self.path)
        batch.add_copy_command(self.path, target)
        console.info('Restoring to: %s' % target)

    def build_compare_batch(self, batch):   #pylint: disable=no-self-use,unused-argument
        """Populate a command batch for comparing against the archive."""
        console.abort('Compare is not yet implemented for uncompressed archive items.')
