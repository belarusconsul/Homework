### Task 1.4
### Write a Python program to sort a dictionary by key.


def sort_dictionary_by_key(input_dict):
    return dict(sorted(input_dict.items()))


# =============================================================================
# test_dict = {2: 20, 3: 30, 5: 50, 4: 40, 1: 10}
# print(sort_dictionary_by_key(test_dict))
# =============================================================================
