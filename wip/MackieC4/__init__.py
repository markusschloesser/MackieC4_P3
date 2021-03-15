# Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/__init__.py
# Compiled at: 2011-01-12 06:17:37
# Decompiled by https://python-decompiler.com
from __future__ import absolute_import, print_function, unicode_literals  # MS
from .MackieC4 import MackieC4


def create_instance(c_instance):
    return MackieC4(c_instance)


from _Framework.Capabilities import *


# def get_capabilities():
#    return {GENERIC_SCRIPT_KEY: True}