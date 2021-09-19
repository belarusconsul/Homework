# Task 4.6
# Implement a function get_longest_word(s: str) -> str which returns
# the longest word in the given string. The word can contain any symbols
# except whitespaces ( , \n, \t and so on). If there are multiple longest
# words in the string with a same length return the word that occures first.


def get_longest_word(s):
    """
    Return the longest word in a string

    Parameters
    ----------
    s : TYPE string
        DESCRIPTION : any string

    Returns
    -------
    result : TYPE string
        DESCRIPTION : longest word in the input string.
                      If there are multiple longest words in the string
                      return the word that occures first.

    """
    list_of_words = s.split()
    len_max = 0
    result = ""
    for word in list_of_words:
        if len(word) > len_max:
            result = word
            len_max = len(word)
    return result


# =============================================================================
# print(get_longest_word('Python\nis\tsimple and effective!'))
# print(get_longest_word('Any pythonista like namespaces a lot.'))
# =============================================================================
