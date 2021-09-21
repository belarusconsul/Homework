# Task 4.5
# Implement a decorator remember_result which remembers last result of
# function it decorates and prints it before next call.


def remember_result(function, last=[None]):
    """
    Decorator which remembers last result of function it decorates
    and prints it before next call.

    Parameters
    ----------
    function : TYPE function
        DESCRIPTION. Decorated function
    last : TYPE list, optional
        DESCRIPTION. Result of previous function call. The default is [None].

    Returns
    -------
    None.

    """
    def wrapper(*args):
        print(f"Last result = '{last[0]}'")
        last[0] = function(*args)
    return wrapper


@remember_result
def sum_list(*args):
    """
    Sum integer arguments or concatenate string arguments.

    Parameters
    ----------
    *args : TYPE integer or string.
        DESCRIPTION. Values to sum or concatenate.

    Returns
    -------
    result : TYPE string
        DESCRIPTION. Result of summing or concatenating of arguments.

    """
    try:
        result = str(sum(args))
    except TypeError:
        result = ""
        for item in args:
            result += item
    print(f"Current result = '{result}'")
    return result


# =============================================================================
# sum_list("a", "b")
# sum_list("abc", "cde")
# sum_list(3,4,5)
# =============================================================================
