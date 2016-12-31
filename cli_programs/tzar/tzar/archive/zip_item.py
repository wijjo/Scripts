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

from scriptbase import console

from .base_item import BaseItem

class ZipItem(BaseItem):

    @classmethod
    def item_for_path_if_matching(cls, path, parsed_name, config_data, **kwargs):
        if parsed_name.extension == 'zip':
            return ZipItem(path, config_data, **kwargs)

    def __init__(self, path, config_data, **kwargs):
        BaseItem.__init__(self, path, config_data, **kwargs)

    def build_create_batch(self, batch):
        batch.add_command('zip', '-r', '--symlinks')
        batch.add_args((self.archive, '.zip'), self.path)
        batch.add_exclude_args('--exclude')
        batch.add_source_deletion()

    def build_restore_batch(self, batch):
        console.abort('Restore is not yet implemented for zip compression.')

    def build_compare_batch(self, batch):
        console.abort('Compare is not yet implemented for zip compression.')
