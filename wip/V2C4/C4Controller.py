
from .V2C4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from .C4Model import C4Model


class C4Controller(V2C4Component):

    __module__ = __name__

    def __init__(self, *a, **k):
        V2C4Component.__init__(self, *a, **k)


