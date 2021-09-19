# Task 4.10
# Implement a function that takes a number as an argument and returns
# a dictionary, where the key is a number and the value is the square
# of that number.


def generate_squares(num):
    """
    Return a dictionary of all squares up to the input number

    Parameters
    ----------
    num : TYPE integer
        DESCRIPTION : any positive integer

    Returns
    -------
    TYPE dictionary
        DESCRIPTION : dictionary of all squares up to the input number.
    """
    return {i: i ** 2 for i in range(1, num + 1)}


# =============================================================================
# print(generate_squares(5))
# =============================================================================
