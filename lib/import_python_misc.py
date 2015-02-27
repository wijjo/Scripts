import sys
import os

# Look for python_misc under a parent folder.
folder = os.path.dirname(os.path.dirname(__file__))
while not os.path.exists(os.path.join(folder, 'python_misc', 'python_misc', '__init__.py')):
    folder = os.path.dirname(folder)
    if folder == '/':
        sys.stderr.write('''
python_misc library not found
''')
        sys.exit(1)
path = os.path.join(folder, 'python_misc')
if not path in sys.path:
    sys.path.insert(0, path)
