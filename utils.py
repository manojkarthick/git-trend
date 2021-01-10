from traceback import format_tb

from prettytable import PrettyTable

from enums import Periods, Formats
from languages import get_languages_json, get_spoken_languages_json


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


def get_supported_languages_v0():
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


def get_supported_languages():
    language_info = get_languages_json()
    languages = []
    for info in language_info:
        languages.append(info["urlParam"])
    return languages


def get_supported_spoken_languages():
    language_info = get_spoken_languages_json()
    languages = []
    for info in language_info:
        languages.append(info["urlParam"])
    return languages


def print_supported_languages(dtype="programming"):
    tbl = PrettyTable()

    language_info = None
    if dtype == "programming":
        tbl.field_names = ["Language Name", "Language Code"]
        language_info = get_languages_json()
    elif dtype == "spoken":
        tbl.field_names = ["Spoken Language Name", "Spoken Language Code"]
        language_info = get_spoken_languages_json()
    else:
        print("ERROR: Unknown data type provided. Exiting.")
        exit(1)

    for info in language_info:
        language_code = info["urlParam"]
        language_name = info["name"]
        tbl.add_row([language_name, language_code])
    tbl.align = "l"
    print(tbl)


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
        return False
    else:
        return True


def get_traceback_string(e):
    """
    Get the traceback associated with a given exception
    :param e: the exception whose traceback is needed
    :return:
    """
    return ''.join(format_tb(e.__traceback__))
