from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import object, range, str

from .C4_DEFINES import *

# can't import like this, circular dependency city
# from .V2C4 import V2C4



class V2C4Component(object):
    """ Baseclass for every specialized 'subcomponent' of the Mackie C4 in this V2 script.
        This class allows inheriting subclasses to reference public methods of the V2C4
        ControlSurface class as if they were referencing inherited methods of V2C4Component
         (because they are inheriting methods of V2C4Component)"""
    __module__ = __name__

    def __init__(self):
        self._script_backdoor = None

    def destroy(self):
        pass

    def _set_script_backdoor(self, main_script):
        # can't validate like this because can't import V2C4
        # assert isinstance(main_script, V2C4)
        self._script_backdoor = main_script

    def _log_message(self, *message):
        """ Overrides ControlSurface standard to only use python logger and not also c_instance logger """
        try:
            message = '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, message)))
            self._script_backdoor.get_logger().info(message)
        except:
            self._script_backdoor.get_logger().info('Logging encountered illegal character(s)!')
