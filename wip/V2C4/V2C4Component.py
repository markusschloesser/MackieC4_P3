from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import object

from .C4_DEFINES import *

from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class V2C4Component(ControlSurfaceComponent):
    """Baseclass for every 'subcomponent' of the Mackie C4 in this V2 script"""
    __module__ = __name__

    # don't really know what these pointers represent, but all the
    # _Framework classes pass them around
    def __init__(self, *a, **k):
        ControlSurfaceComponent.__init__(self, *a, **k)
        self.__a = a
        self.__k = k

    def destroy(self):
        pass
