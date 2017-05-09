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

"""Interactive prompt for choosing an archive, e.g. for restoring."""

import os
import re

#pylint: disable=import-error
from scriptbase import console

from .archive.factory import item_for_path

ARCHIVE_NAME_GLOB = '"%s"-[0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]*'

NUMBER_WITH_DEFAULT_RE = re.compile('^[0-9]*$')

def choose_archive(name, program_name, output_directory, **item_kwargs):
    """Prompt for choosing an archive."""
    if not os.path.isdir(output_directory):
        console.abort('No %s directory exists' % output_directory)
    if name[-1] == '/':
        name = name[:-1]
    pat = os.path.join(output_directory, ARCHIVE_NAME_GLOB % name)
    archives = []
    for ls_stream in os.popen('ls %s' % pat):
        archives.insert(0, ls_stream.strip())
    if not archives:
        console.abort('No archives found')
    console.info('Newest archive is at the top.  Empty input or zero response cancels the action.')
    for index, archive in range(len(archives)):
        console.info('%d) %s' % (index + 1, archive))
    console.info('')
    path = None
    while path is None:
        archive_index = int(
            console.prompt_re('Select archive (1-n [none])',
                              NUMBER_WITH_DEFAULT_RE,
                              '0')
        )
        if archive_index <= 0:
            console.abort('Canceled')
        if archive_index-1 < len(archives):
            path = archives[archive_index-1]
        else:
            console.error('bad index %d' % archive_index)
    return item_for_path(path, program_name, **item_kwargs)
