# Task 4.2
# Implement a function which search for most common words in the file.
# Use data/lorem_ipsum.txt file as a example.


def most_common_words(filepath, number_of_words=3):
    """
    Return the most common words in the file.

    Parameters
    ----------
    filepath : TYPE string
        DESCRIPTION. Path to a file
    number_of_words : TYPE integer, optional
        DESCRIPTION. Number of words to return. The default is 3.

    Returns
    -------
    list_of_words : TYPE list
        DESCRIPTION. Most common words in the file.

    """
    dic_of_words = {}
    with open(filepath, "r") as f:
        list_of_words = f.read().lower().split()
        for word in list_of_words:
            if not word.isalpha():
                word = "".join([char for char in word if char.isalpha()])
            dic_of_words[word] = dic_of_words.get(word, 0) + 1
    list_of_words = sorted(dic_of_words, key=dic_of_words.get, reverse=True)[
        :number_of_words
    ]
    return list_of_words


# =============================================================================
# print(most_common_words("data/lorem_ipsum.txt"))
# =============================================================================
