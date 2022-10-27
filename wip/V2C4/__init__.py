
from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from .V2C4 import V2C4

def create_instance(c_instance, *a, **k):
    return V2C4(c_instance, *a, **k)