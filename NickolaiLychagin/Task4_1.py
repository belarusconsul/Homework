### Task 4.1
### Implement a function which receives a string and replaces
### all " symbols with ' and vise versa.


def replace_quotation(input_string):
    """
    Replace all " symbols in input_string with ' and vise versa.

    Parameters
    ----------
    input_string : TYPE string
        DESCRIPTION : any string.

    Returns
    -------
    result : TYPE string
        DESCRIPTION : string with replaced " and ' symbols.

    """

    result = ""
    for char in input_string:
        if char == "'":
            result += '"'
        elif char == '"':
            result += "'"
        else:
            result += char
    return result


# =============================================================================
# test_string = "In this string there are \"single quotation marks\" \
# and 'double quotation marks'"
# print(replace_quotation(test_string))
# =============================================================================
