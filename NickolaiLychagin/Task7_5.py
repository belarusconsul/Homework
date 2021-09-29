# Task 7.5
# Implement function for check that number is even and is greater than 2.
# Throw different exceptions for this errors. Custom exceptions must be
# derived from custom base exception(not Base Exception class).


class WrongAttribute(Exception):
    """
    Custom base exception
    """

    pass


class NumberTooSmall(WrongAttribute):
    """
    Custom exception if a number is too small
    """

    pass


class NotANumber(WrongAttribute):
    """
    Custom exception if an attribute is not a number
    """

    pass


class NotAnInteger(WrongAttribute):
    """
    Custom exception if a float can't be interpreted as integer
    """

    pass


def check_even(number):
    """
    Check that number is even and is greater than 2.

    Parameters
    ----------
    number : TYPE integer
        DESCRIPTION. Any integer greater than 2.

    Raises
    ------
    NotAnInteger
        DESCRIPTION. Custom exception if a float can't be interpreted as integer.
    NumberTooSmall
        DESCRIPTION. Custom exception if a number is smaller than 3.
    NotANumber
        DESCRIPTION. Custom exception if an attribute is not a number

    Returns
    -------
    TYPE boolean
        DESCRIPTION. True if number is even, false - otherwise.

    """
    try:
        number = float(number)
        if number != int(number):
            raise NotAnInteger("Number must be an integer greater than 2")
        if number < 3:
            raise NumberTooSmall("Number must be greater than 2")
        return number % 2 == 0
    except ValueError:
        raise NotANumber("Number must be an integer greater than 2") from ValueError


# =============================================================================
# print(check_even(4))
# print(check_even(5))
# print(check_even(1))
# print(check_even("4"))
# print(check_even("a"))
# print(check_even(4.0))
# print(check_even("4.5"))
# =============================================================================
