import sys
import os

# Where to look for scriptbase/__init__.py under parent directories.
BASE_SUB_DIRS = ('lib', os.path.join('ext', 'scriptbase'))

def add_scriptbase_to_sys_path():
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
    import scriptbase.utility
except ImportError:
    add_scriptbase_to_sys_path()
