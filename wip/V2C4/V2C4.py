

from __future__ import absolute_import, print_function, unicode_literals
import sys

from _Framework.ControlSurface import ControlSurface

from .C4Controller import C4Controller


if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object

class V2C4(ControlSurface):
    """V2C4 class acts as a container/manager for all the
       C4 subcomponents like Encoders, Displays and so on.
       V2C4 is glued to Live's MidiRemoteScript C instance"""
    __module__ = __name__

    def __init__(self, c_instance, *a, **k):
        ControlSurface(c_instance, *a, **k)
        self.__c_instance = c_instance
        self.__controller = C4Controller(self, *a, **k)
