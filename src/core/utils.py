import sys
import argparse

from itertools import cycle
from knack.log import get_logger
from knack.cli import CLIError
from knack.arguments import CLIArgumentType, CaseInsensitiveList

from core.constants import ANSI_ERASE_LINE, ANSI_HIDE_CURSOR, ANSI_SHOW_CURSOR


logger = get_logger(__name__)



def _clear_line_and_show_cursor():
    return sys.stderr.write(f"\r{ANSI_ERASE_LINE}{ANSI_SHOW_CURSOR}")

def long_running_operations_handler(lro, **kwargs):
    from sys import stderr
  
    spinner = cycle(['|','/','-','\\'])

    label ='Starting'

    try:
        while lro.status() == "InProgress":
            if lro.status() != "InProgress":
                break
            
            stderr.write(f"{ANSI_ERASE_LINE}{ANSI_HIDE_CURSOR}{next(spinner)} {label}\r")
            lro.wait(.2)
            label = 'Running...'

        _clear_line_and_show_cursor()
    except KeyboardInterrupt:
        _clear_line_and_show_cursor()
        logger.error('Long running operation canceled...')
        raise
    except Exception as e:
        _clear_line_and_show_cursor()
        raise e
    return lro.result()

def get_enum_type(data, default=None):
    """ Creates the argparse choices and type kwargs for a supplied enum type or list of strings. """
    if not data:
        return None

    # transform enum types, otherwise assume list of string choices
    try:
        choices = [x.value for x in data]
    except TypeError:
        choices = data

    # pylint: disable=too-few-public-methods
    class DefaultAction(argparse.Action):

        def __call__(self, parser, args, values, option_string=None):

            def _get_value(val):
                return next((x for x in self.choices if x.lower() == val.lower()), val)

            if isinstance(values, list):
                values = [_get_value(v) for v in values]
            else:
                values = _get_value(values)
            setattr(args, self.dest, values)

    def _type(value):
        return next((x for x in choices if x.lower() == value.lower()), value) if value else value

    default_value = None
    if default:
        default_value = next((x for x in choices if x.lower() == default.lower()), None)
        if not default_value:
            raise CLIError("Command authoring exception: unrecognized default '{}' from choices '{}'"
                           .format(default, choices))
        arg_type = CLIArgumentType(choices=CaseInsensitiveList(choices), action=DefaultAction, default=default_value)
    else:
        arg_type = CLIArgumentType(choices=CaseInsensitiveList(choices), action=DefaultAction)
    return arg_type