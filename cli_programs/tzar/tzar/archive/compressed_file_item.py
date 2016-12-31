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

class CompressedFileItem(BaseItem):

    @classmethod
    def item_for_path_if_matching(cls, path, parsed_name, config_data, **kwargs):
        if parsed_name.extension == 'gz':
            return CompressedFileItem(path, 'gzip', config_data, **kwargs)
        if parsed_name.extension == 'bz2':
            return CompressedFileItem(path, 'bzip2', config_data, **kwargs)
        if parsed_name.extension == 'xz':
            return CompressedFileItem(path, 'xz', config_data, **kwargs)
        if parsed_name.extension == 'lz':
            return CompressedFileItem(path, 'lzip', config_data, **kwargs)

    def __init__(self, compression, config_data, **kwargs):
        BaseItem.__init__(self, path, config_data, **kwargs)
        self.compression = compression

    def build_create_batch(self, batch):
        batch.add_move_or_copy_archive_command()
        batch.add_archive_compression_command()

    def build_restore_batch(self, batch):
        console.abort('Restore is not yet implemented for compressed files.')

    def build_compare_batch(self, batch):
        console.abort('Compare is not yet implemented for compressed files.')
