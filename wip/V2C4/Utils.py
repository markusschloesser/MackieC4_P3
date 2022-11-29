# copied from open source _NKFW2/Utils.py and ControlUtils.py

import Live, datetime
from _Framework.Util import find_if
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent


def date_has_passed(date):
    """ Returns whether the date in the form of (month, year) has passed. """
    now = datetime.datetime.now()
    current_date = (now.month, now.year)
    year_comp = current_date[1] > date[1]
    year_equal = current_date[1] == date[1]
    month_comp = current_date[0] > date[0]
    if year_comp or year_equal and month_comp:
        return True
    return False


def format_absolute_time(element, time, base_is_one=True):
    """ Returns a string representing the given absolute time as bars.beats.sixteenths.
        Can specify whether the base for displaying is one or zero."""
    assert isinstance(element, (Live.Clip.Clip, Live.Song.Song))
    assert isinstance(time, float)
    base = int(base_is_one)
    beat_length = 4.0 / element.signature_denominator
    bar_length = beat_length * element.signature_numerator
    bar = int(time / bar_length) + base
    beat = int(time / beat_length % element.signature_numerator) + base
    teenth_as_float = time % beat_length / 0.25 + base
    teenth_as_int = int(teenth_as_float)
    teenth_plus = ''
    if teenth_as_float % 1.0 != 0.0:
        teenth_plus = '+'
    return '%s.%s.%s%s' % (bar, beat, teenth_as_int, teenth_plus)


def calculate_bar_length(obj):
    """ Returns the length of a bar at the current time signature. """
    return 4.0 / obj.signature_denominator * obj.signature_numerator


def calculate_beat_length(obj):
    """ Returns the length of a beat at the current time signature. """
    return 4.0 / obj.signature_denominator


def parse_file(file_name, file_path, logger=None, to_upper=True):
    """ Reads the given file name from the given path and returns a dict of
    the keys and values it contains. """
    file_to_read = file_path + '/' + file_name
    try:
        with open(file_to_read) as (f):
            if logger:
                logger('Attempting to read %s' % file_to_read)
            file_data = {}
            for line in f:
                if '=' in line and not line.startswith('#'):
                    data = line.split('=')
                    if len(data) == 2:
                        if logger:
                            logger(str(line))
                        file_data[data[0].strip()] = data[1].upper().strip() if to_upper else data[1].strip()

            return file_data
    except IOError:
        if logger:
            logger('%s is missing!' % file_to_read)


def parse_int(int_as_string, default_value=None, min_value=None, max_value=None):
    """ Parses the given string containing an int and returns the parsed int. If a parse
    error occurs, the default_value will be returned. If a min_value or max_value is
    given, the default_value will be returned if the parsed_value is not within range. """
    ret_value = default_value
    try:
        parsed_value = int(int_as_string)
        if min_value is not None and parsed_value < min_value:
            return ret_value
        if max_value is not None and parsed_value > max_value:
            return ret_value
        ret_value = parsed_value
    except:
        pass

    return ret_value


def floats_equal(a, b, rel_tol=1e-09, abs_tol=0.0):
    """ Returns True if the given floats are close to being equal. """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def live_object_is_valid(obj):
    """ Returns True if the given object is still present and not a lost
    weak reference. """
    if isinstance(obj, ControlSurfaceComponent) and obj.name == 'Track_Mixer_Device':
        return obj.track is not None
    else:
        return obj is not None


# ControlUtils
UNLISTED_QUANTIZED_PARAMETERS = {
    'MidiArpeggiator': ('Synced Rate', 'Ret. Interval', 'Repeats', 'Transp. Steps'),
    'MidiNoteLength': ('Synced Length', ),
    'MidiScale': ('Base', ),
    'BeatRepeat': ('Interval', 'Offset', 'Grid', 'Variation', 'Gate', 'Pitch'),
    'UltraAnalog': ('OSC1 Octave', 'OSC2 Octave'),
    'StringStudio': ('Octave', ),
    'GlueCompressor': ('Ratio', 'Attack', 'Release', 'Peak Clip In')}


def release_parameters(controls):
    """ Releases the parameters the given controls are attached to. """
    if controls is not None:
        for control in controls:
            if control is not None:
                control.release_parameter()
                control._parameter_to_map_to = None

    return


def can_reset_or_toggle_parameter(param):
    """ Returns True if the parameter value can be reset or toggled. """
    already_default = floats_equal(param.value, param.default_value)
    if param is not None:
        return param.is_enabled and (parameter_is_quantized(param) or not already_default)
    else:
        return False


def reset_parameter(param):
    """ Scrolls quantized parameter values with wrap around, else resets param value to default """
    if param and param.is_enabled:
        if parameter_is_quantized(param):
            if param.value + 1 > param.max:
                param.value = param.min
            else:
                param.value = param.value + 1
        else:
            param.value = param.default_value


def get_parameter_value_to_set(param, value):
    """ Returns either the value that was passed or the parameter's min/max value if
    the passed value is out of range. """
    assert param is not None and isinstance(value, float)
    if value > param.max:
        value = param.max
    else:
        if value < param.min:
            value = param.min
    return value



def parameter_value_to_midi_value(p_value, p_min, p_max):
    """ Returns a valid MIDI value for the given parameter value/range. """
    if p_min > p_max or p_value < p_min:
        return 0
    p_range = p_max - p_min
    return abs(min(127, int(float(p_value - p_min) / p_range * 128.0)))


def parameter_is_quantized(param):
    """ Returns True if the given parameter is quantized. This is needed
    for cases where parameters are quantized, but are not listed that way. """
    if live_object_is_valid(param):
        if param.is_quantized:
            return True
        parent = param.canonical_parent
        if isinstance(parent, Live.Device.Device):
            parent = parent.class_name
            return parent in UNLISTED_QUANTIZED_PARAMETERS and param.name in UNLISTED_QUANTIZED_PARAMETERS[parent]
    return False
