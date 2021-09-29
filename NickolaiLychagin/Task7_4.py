# Task 7.4
# Implement decorator for supressing exceptions. If exception not occure
# write log to console.


def suppress_exception(function):
    """
    Decorator for supressing exceptions. If exception does not occur
    write log to console.

    Parameters
    ----------
    function : TYPE function.
        DESCRIPTION. Function to be decorated.

    Returns
    -------
    TYPE function
        DESCRIPTION. Decorated function.

    """

    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
        except Exception:
            pass
        else:
            print(f"Operation on '{function.__name__}' finished successfully\n")
            return result

    return wrapper


# =============================================================================
# @suppress_exception
# def dumb_func():
#     for i in range(1000000):
#         pass
# @suppress_exception
# def div_zero():
#     return 2/0
# 
# dumb_func()
# div_zero()
# =============================================================================
