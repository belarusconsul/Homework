# Task 4.6
# Implement a decorator call_once which runs a function or method once
# and caches the result. All consecutive calls to this function should
# return cached result no matter the arguments.


def call_once(function, last=[None]):
    """
    Decorator which caches the result of the first function call.
    All consecutive calls to this function return cached result.

    Parameters
    ----------
    function : TYPE function
        DESCRIPTION. Decorated function
    last : TYPE list, optional
        DESCRIPTION. Result of previous function call. The default is [None].

    Returns
    -------
    Cached result of the first function call.

    """
    def wrapper(*args):
        if not last[0]:
            last[0] = function(*args)
        return last[0]
    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b


# =============================================================================
# print(sum_of_numbers(13, 42))
# print(sum_of_numbers(999, 100))
# print(sum_of_numbers(134, 412))
# print(sum_of_numbers(856, 232))
# =============================================================================
