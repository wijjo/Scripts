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

"""Factory creation of archive items."""

import re

#pylint: disable=import-error
from scriptbase import console

from .compressed_file_item import CompressedFileItem
from .uncompressed_item import UncompressedItem
from .p7zip_item import P7ZipItem
from .tarball_item import TarballItem
from .zip_item import ZipItem

TRAILER_PAT = r'^[.]%s/(.*)-([0-9]+-[0-9]+)(?:[.](tar))?[.](\w+)$'

class _ParsedName(object):
    def __init__(self, base_path, time_string, extension_prefix, extension):
        self.base_path = base_path
        self.time_string = time_string
        self.extension = extension
        self.extension_prefix = extension_prefix

def item_for_path(path, program_name, config_data, **item_kwargs):
    """Create an appropriate archive item for a path."""
    for item_cls in (
            TarballItem,
            ZipItem,
            P7ZipItem,
            UncompressedItem,
            CompressedFileItem,
    ):
        matched = re.match(TRAILER_PAT % program_name, path)
        if matched:
            parsed_name = _ParsedName(*matched.groups())
        else:
            parsed_name = _ParsedName(path, None, None, None)
        item = item_cls.item_for_path_if_matching(path, parsed_name, config_data, **item_kwargs)
        if item:
            return item
    console.abort('"%s" is not a supported type' % path)
