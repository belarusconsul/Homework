# Task 4.7
# Implement a function foo(List[int]) -> List[int] which, given a list
# of integers, return a new list such that each element at index i of
# the new list is the product of all the numbers in the original array
# except the one at i.


def foo(list_of_int):
    """
    Given a list of integers, return a new list such that each element
    at index i of the new list is the product of all the numbers in the
    original array except the one at i.

    Parameters
    ----------
    list_of_int : TYPE list
        DESCRIPTION : list of positive integers

    Returns
    -------
    result : TYPE list
        DESCRIPTION : list that is the product of all the numbers in the
        original list except the one at i

    """
    result = []
    for i in range(len(list_of_int)):
        mult = 1
        for j in range(len(list_of_int)):
            if i == j:
                continue
            mult *= list_of_int[j]
        result.append(mult)
    return result


# =============================================================================
# print(foo([1, 2, 3, 4, 5]))
# print(foo([3, 2, 1]))
# =============================================================================
