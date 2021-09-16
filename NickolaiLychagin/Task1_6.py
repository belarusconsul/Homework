### Task 1.6
### Write a Python program to convert a given tuple of positive integers into an integer.


def convert_to_integer(input_tuple):
    to_string = ""
    for number in input_tuple:
        to_string += str(number)
    return int(to_string)


# =============================================================================
# test_tuple = (1, 2, 3, 4)
# print(convert_to_integer(test_tuple))
# =============================================================================
