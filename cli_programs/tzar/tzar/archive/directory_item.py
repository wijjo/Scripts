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

from scriptbase import console
from scriptbase import disk

from .base_item import BaseItem

class DirectoryItem(BaseItem):

    @classmethod
    def item_for_path_if_matching(cls, path, parsed_name, config_data, **kwargs):
        if os.path.isdir(path):
            return DirectoryItem(path, config_data, **kwargs)

    def __init__(self, path, config_data, **kwargs):
        BaseItem.__init__(self, path, config_data, **kwargs)

    def build_create_batch(self, batch):
        batch.add_move_or_copy_archive_command()

    def build_restore_batch(self, batch):
        target = disk.get_versioned_path(self.path)
        batch.add_copy_command(self.path, target)
        console.info('Restoring to "%s"...' % target)

    def build_compare_batch(self, batch):
        console.abort('Compare is not yet implemented for archived directories.')
