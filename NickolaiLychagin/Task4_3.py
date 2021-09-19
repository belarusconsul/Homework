# Task 4.3
# Implement a function which works the same as str.split method
# (without using str.split itself, of course).


def split_string(input_string, separator=" "):
    """
    Split string into list of words according to separator.

    Parameters
    ----------
    input_string : TYPE string
        DESCRIPTION : any string
    separator : TYPE string, optional
        DESCRIPTION : The default is " ".

    Returns
    -------
    list_of_words : TYPE list
        DESCRIPTION : list of words the string is splitted into.

    """

    list_of_words = []
    string_to_go = input_string if separator.strip() else input_string.strip()
    while string_to_go:
        end = string_to_go.find(separator)
        if end == -1:
            list_of_words.append(string_to_go)
            break
        else:
            list_of_words.append(string_to_go[:end])
            word_left = string_to_go[end + len(separator) :]
            string_to_go = word_left if separator.strip() else word_left.strip()
    if not string_to_go:
        list_of_words.append(string_to_go)
    return list_of_words


# =============================================================================
# test_string = "Hello world"
# print(test_string.split())
# print(split_string(test_string))
# test_string = "Hello world"
# print(test_string.split("   "))
# print(split_string(test_string, "   "))
# test_string = "***Hello***world***"
# print(test_string.split("***"))
# print(split_string(test_string, "***"))
# test_string = "   aaa  bb   "
# print(test_string.split())
# print(split_string(test_string))
# test_string = ",,,aaa,,bb,,,"
# print(test_string.split(','))
# print(split_string(test_string, ','))
# =============================================================================
