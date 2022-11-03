#__init__.py

from .MackieC4_v3 import MackieC4_v3


def create_instance(c_instance):
    return MackieC4_v3(c_instance=c_instance)