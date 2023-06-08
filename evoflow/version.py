import os

root = os.path.dirname(os.path.abspath(__file__))
__version__ = open(os.path.join(root, "VERSION")).read().strip()
