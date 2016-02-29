import sys
import os

# Look for python_misc under ext or the parent folder.
python_misc = None
repo_root = os.path.dirname(os.path.dirname(__file__))
for base in (os.path.join(repo_root, 'ext'), os.path.dirname(repo_root)):
    python_misc_chk = os.path.join(base, 'python_misc')
    if os.path.exists(os.path.join(python_misc_chk, 'python_misc', '__init__.py')):
        python_misc = python_misc_chk
        break
else:
    sys.stderr.write('''
python_misc library not found
''')
    sys.exit(1)
if python_misc not in sys.path:
    sys.path.insert(0, python_misc)
