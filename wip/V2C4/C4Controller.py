
from .V2C4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from .C4_DEFINES import *
from .C4Model import C4Model
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement


class C4Controller(V2C4Component):

    __module__ = __name__

    def __init__(self, *a, **k):
        V2C4Component.__init__(*a, **k)
        self.__lcd_00 = PhysicalDisplayElement(*a, **k)
        self.__lcd_01 = PhysicalDisplayElement(*a, **k)
        self.__lcd_02 = PhysicalDisplayElement(*a, **k)
        self.__lcd_03 = PhysicalDisplayElement(*a, **k)
        self.__model = C4Model(*a, **k)

