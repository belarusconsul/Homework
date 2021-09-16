### Task 1.3
### Write a Python program that accepts a comma separated sequence of words as input and prints the unique words in sorted form.


def get_sorted_unique_words(list_of_words):
    print(sorted(set(list_of_words)))


# =============================================================================
# test_list = ['red', 'white', 'black', 'red', 'green', 'black']
# get_sorted_unique_words(test_list)
# =============================================================================
