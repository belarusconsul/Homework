# Task 4.4
# Implement a function split_by_index(s: str, indexes: List[int]) -> List[str]
# which splits the s string by indexes specified in indexes. 
# Wrong indexes must be ignored.


def split_by_index(s, indexes):
    """
    Split string by indexes.

    Parameters
    ----------
    s : TYPE string
        DESCRIPTION : any string
    indexes : TYPE list
        DESCRIPTION : list on integers

    Returns
    -------
    result : TYPE list
        DESCRIPTION : list of strings that the input string is splitted into

    """
    result = []
    start = 0
    for ind in indexes:
        result.append(s[start:ind])
        start = ind
    if s[ind:]:
        result.append(s[ind:])
    return result


# =============================================================================
# print(split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18]))
# print(split_by_index("no luck", [42]))
# =============================================================================
