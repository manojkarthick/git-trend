from traceback import format_tb

from enums import Periods, Formats


def get_supported_periods():
    """
    Return the time periods supported by the program
    :return:
    """
    return [e.value for e in Periods]


def get_supported_formats():
    """
    Return the output formats supported by the program
    :return:
    """
    return [e.value for e in Formats]


def get_supported_languages():
    """
    Return the programming languages supported by the program
    :return:
    """
    return [
        'python',
        'ruby',
        'c',
        'c++',
        'java',
        'scala',
        'kotlin',
        'javascript',
        'typescript',
        'go',
        'rust',
        'lua',
        'haskell'
    ]


def strip_and_get(val, fallback=""):
    """
    Return the enclosing text or provided fallback value
    :param val: item to get text and strip whitespace
    :param fallback: fallback when val is None
    :return: stripped text value
    """
    if val:
        return val.text.strip(' \t\n\r')
    else:
        return fallback


def check_if_list_valid(items, content_type):
    """
    Check if the passed items list is valid, Valid if length is greater than one.
    :param items: Items to check
    :param content_type: Type of content to parse
    :return:
    """
    if len(items) < 1:
        print("Could not get trending {} from the page.".format(content_type))
        print("ERROR: Raise an issue on https://github.com/manojkarthick/git-trend/issues")
        exit(1)


def get_traceback_string(e):
    """
    Get the traceback associated with a given exception
    :param e: the exception whose traceback is needed
    :return:
    """
    return ''.join(format_tb(e.__traceback__))
