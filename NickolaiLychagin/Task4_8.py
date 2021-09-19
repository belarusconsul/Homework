# Task 4.8
# Implement a function get_pairs(lst: List) -> List[Tuple] which returns
# a list of tuples containing pairs of elements. Pairs should be formed
# as in the example. If there is only one element in the list return None instead.


def get_pairs(lst):
    """
    Return a list of tuples containing pairs of elements in the input list.

    Parameters
    ----------
    lst : TYPE list
        DESCRIPTION : list of any elements.

    Returns
    -------
    result : TYPE list
        DESCRIPTION : list of tuples containing pairs of elements in the input list

    """
    result = []
    lst_copy = lst.copy()
    if len(lst_copy) <= 1:
        return None
    while len(lst_copy) > 1:
        first, second = lst_copy.pop(0), lst_copy[0]
        result.append((first, second))
    return result


# =============================================================================
# print(get_pairs([1, 2, 3, 8, 9]))
# print(get_pairs(['need', 'to', 'sleep', 'more']))
# print(get_pairs([1]))
# =============================================================================
