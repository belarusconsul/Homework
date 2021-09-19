# Task 4.11
# Implement a function, that receives changeable number of dictionaries
# (keys - letters, values - numbers) and combines them into one dictionary.
# Dict values ​​should be summarized in case of identical keys


def combine_dicts(*args):
    """
    Combine values of identical keys in several dictionaries

    Parameters
    ----------
    *args : TYPE dictionary
        DESCRIPTION : changeable number of dictionaries.

    Returns
    -------
    result : TYPE dictionary
        DESCRIPTION : dictionary of combined values of identical keys in input dictionaries

    """
    result = {}
    for dictionary in args:
        for k, v in dictionary.items():
            result[k] = result.get(k, 0) + v
    return result


# =============================================================================
# dict_1 = {"a": 100, "b": 200}
# dict_2 = {"a": 200, "c": 300}
# dict_3 = {"a": 300, "d": 100}
# print(combine_dicts(dict_1, dict_2))
# print(combine_dicts(dict_1, dict_2, dict_3))
# =============================================================================
