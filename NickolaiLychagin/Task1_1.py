### Task 1.1
### Write a Python program to calculate the length of a string without using the `len` function.


def get_string_length(input_string):
    length = 0
    for char in input_string:
        length += 1
    return length


def get_string_length_ind(input_string):
    last_char = input_string[-1]
    return input_string.index(last_char, -1) + 1


# =============================================================================
# test_string = "Python is a programming language that lets you work quickly \
# and integrate systems more effectively."
# print(len(test_string))
# print(get_string_length(test_string))
# print(get_string_length_ind(test_string))
# =============================================================================
