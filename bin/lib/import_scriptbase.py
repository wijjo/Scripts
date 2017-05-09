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

"""Set up sys.path for access to scriptbase modules."""

import sys
import os

# Where to look for scriptbase/__init__.py under parent directories.

BASE_SUB_DIRS = ('lib', os.path.join('ext', 'scriptbase'))
def _add_scriptbase_to_sys_path():
    # Look for lib/scriptbase or ext/scriptbase/scriptbase in the directory hierarchy.
    last_base_dir = None
    base_dir = os.path.dirname(os.path.dirname(__file__))
    while True:
        for base_sub_dir in BASE_SUB_DIRS:
            base_lib_dir = os.path.join(base_dir, base_sub_dir)
            if os.path.exists(os.path.join(base_lib_dir, 'scriptbase', '__init__.py')):
                if base_lib_dir not in sys.path:
                    sys.path.insert(0, base_lib_dir)
                return
        base_dir = os.path.dirname(base_dir)
        # Let the ImportException happen.
        if not base_dir or base_dir == last_base_dir:
            return
        last_base_dir = base_dir

try:
    # Do nothing if it imports using the existing system path.
    import scriptbase.utility   #pylint: disable=unused-import
except ImportError:
    _add_scriptbase_to_sys_path()
