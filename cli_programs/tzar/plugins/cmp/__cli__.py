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

"""CLI implementation for "cmp" sub-command."""

#pylint: disable=import-error
from scriptbase.cli import Command, String
from tzar.archive.base_item import option_attributes_to_dictionary
from tzar.choose import choose_archive

@Command(
    name='cmp',
    description='Compare with archive.',
    args=[
        String('path', 'path(s) to compare', nargs='+'),
    ]
)
def _(runner):
    for name in runner.arg.path:
        item = choose_archive(name, **option_attributes_to_dictionary(runner.arg))
        item.compare(runner)
