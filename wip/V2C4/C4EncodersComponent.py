from .V2C4Component import *

from .C4ChannelStripComponent import C4ChannelStripComponent
from .C4Encoders import C4Encoders


class C4EncodersComponent(C4ChannelStripComponent, V2C4Component, C4Encoders):

    __module__ = __name__

    def __init__(self):
        C4ChannelStripComponent.__init__(self)
        V2C4Component.__init__(self)

        # self.encoders_track = None
        self._mapping_encoders = []
        extended_behavior = False
        for i in range(NUM_ENCODERS):
            self._mapping_encoders.append(C4Encoders(self, extended_behavior, i))

    def encoder_components(self):
        return self._mapping_encoders

    # def on_selected_track_changed(self):
    #     if self.is_enabled():
    #         if self.encoders_track is None or self.encoders_track != self.song().view.selected_track:
    #             self.encoders_track = self.song().view.selected_track

    def on_enabled_changed(self):
        self.update()

    def disconnect(self):
        super(C4EncodersComponent, self).disconnect()
        # self.encoders_track = None
        self._mapping_encoders = []

    def set_script_handle(self, main_script):
        """
            need to set this script to call public methods of the V2C4 class
            because they "are" inherited methods of V2C4Component
            to log in Live's log via python only from this or subclasses, for example,
            call self._log_message("message") after setting the script handle here
        """
        self._set_script_handle(main_script)