
from .V2C4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *

class C4EncoderElement(EncoderElement):
    """modeled on Axiom Peekable Encoder Element"""
    __module__ = __name__

    def __init__(self, msg_type, channel, identifier, map_mode):
        EncoderElement.__init__(self, msg_type, channel, identifier, map_mode)
        self._peek_mode = False

    def set_peek_mode(self, peek_mode):
        assert isinstance(peek_mode, type(False))
        if self._peek_mode != peek_mode:
            self._peek_mode = peek_mode
            self._request_rebuild()

    def get_peek_mode(self):
        return self._peek_mode

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        current_parameter = self._parameter_to_map_to
        if self._peek_mode:
            self._parameter_to_map_to = None
        InputControlElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        self._parameter_to_map_to = current_parameter
        return

