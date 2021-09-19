# Task 4.5
# Implement a function get_digits(num: int) -> Tuple[int] which returns 
# a tuple of a given integer's digits.

import math


def get_digits(num):
    """
    Split an integer into a tuple of its digits

    Parameters
    ----------
    num : TYPE integer
        DESCRIPTION : any positive integer

    Returns
    -------
    TYPE tuple
        DESCRIPTION : tuple of input number's integers

    """
    result = []
    try:
        digits = math.ceil(math.log(num, 10))
        for i in range(digits):
            result.append(num // 10 ** i % 10)
        return tuple(result[::-1])
    except ValueError:
        print("Input integer must be a positive number")


# =============================================================================
# print(get_digits(87178291199))
# print(get_digits(-567))
# =============================================================================
