#__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE
from ableton.v2.control_surface.capabilities import SCRIPT, SYNC, controller_id, inport, outport

from .MackieC4_v3 import MackieC4_v3


def create_instance(c_instance, *a, **k):
    return MackieC4_v3(c_inst=c_instance, *a, **k)

def get_capabilities():
    mackie_vendor_id = 2975  # this is the MCU Pro vendor ID
    # mackie_product_id = 6  # this is the MCU Pro product ID
    SYSEX_MACKIE_CONTROL_DEVICE_TYPE_C4 = 0x17
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=mackie_vendor_id,
                                             product_ids=[SYSEX_MACKIE_CONTROL_DEVICE_TYPE_C4],
                                             model_name=['MCU C4']),
            PORTS_KEY: [
                # inport(props=[SCRIPT, REMOTE]),  # from MCU
                # outport(props=[SCRIPT, REMOTE])]}
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),  # from ATOM
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])]}


