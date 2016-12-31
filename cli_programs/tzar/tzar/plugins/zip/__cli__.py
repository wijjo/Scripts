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

from glob import glob
from scriptbase.cli import Command
from tzar.archive.base_item import ARCHIVE_CLI_ARGUMENTS, args_to_kwargs
from tzar.archive.zip_item import ZipItem

@Command(
    name='zip',
    description='Archive with zip compression.',
    args=ARCHIVE_CLI_ARGUMENTS
)
def _(runner):
    for path_pat in runner.arg.path:
        for path in glob(path_pat):
            item = ZipItem(
                        path,
                        runner.cfg.data,
                        **args_to_kwargs(runner.arg)
                   )
            item.create(runner)
