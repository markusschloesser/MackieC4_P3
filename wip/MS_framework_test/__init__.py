# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\__init__.py
# Compiled at: 2021-01-27 15:20:52
# Size of source mod 2**32: 1007 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .C4_framework import C4_framework


def create_instance(c_instance):
    return C4_framework(c_instance=c_instance)
