# Task 4.9
# Implement a bunch of functions which receive a changeable number of strings and return next parameters:
# 1. characters that appear in all strings
# 2. characters that appear in at least one string
# 3. characters that appear at least in two strings
# 4. characters of alphabet, that were not used in any string

import string


def test_1_1(*lst):
    """
    Return characters that appear in all strings

    Parameters
    ----------
    *lst : TYPE string
        DESCRIPTION : changeable number of strings

    Returns
    -------
    TYPE set
        DESCRIPTION : sorted characters that appear in all strings

    """
    num = len(lst)
    dict_of_chars = {}
    for word in lst:
        for char in set(word.lower()):
            dict_of_chars[char] = dict_of_chars.get(char, 0) + 1
    return sorted({k for k, v in dict_of_chars.items() if v == num})


def test_1_3(*lst):
    """
    Return characters that appear at least in two strings

    Parameters
    ----------
    *lst : TYPE string
        DESCRIPTION : changeable number of strings

    Returns
    -------
    TYPE set
        DESCRIPTION : sorted characters that appear at least in two strings

    """
    dict_of_chars = {}
    for word in lst:
        for char in set(word.lower()):
            dict_of_chars[char] = dict_of_chars.get(char, 0) + 1
    return sorted({k for k, v in dict_of_chars.items() if v > 1})


def test_1_2(*lst):
    """
    Return characters that appear in at least one string

    Parameters
    ----------
    *lst : TYPE string
        DESCRIPTION : changeable number of strings

    Returns
    -------
    TYPE set
        DESCRIPTION : sorted characters that appear in at least one string

    """
    return sorted({char for word in lst for char in word.lower()})


def test_1_4(*lst):
    """
    Return characters of alphabet, that were not used in any string

    Parameters
    ----------
    *lst : TYPE string
        DESCRIPTION : changeable number of strings

    Returns
    -------
    TYPE set
        DESCRIPTION : sorted characters of alphabet, that were not used in any string

    """
    return sorted(
        set(string.ascii_lowercase) - {char for word in lst for char in word.lower()}
    )


# =============================================================================
# test_strings = ["hello", "world", "python", ]
# print(test_1_1(*test_strings))
# print(test_1_2(*test_strings))
# print(test_1_3(*test_strings))
# print(test_1_4(*test_strings))
# =============================================================================
