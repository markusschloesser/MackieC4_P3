
from .V2C4Component import *

from .C4Model import C4Model


class C4Controller(V2C4Component):

    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)

    def set_script_backdoor(self, main_script):
        """ to log  in Live's log from this class, for example, need to set this script """
        self._set_script_backdoor(main_script)
