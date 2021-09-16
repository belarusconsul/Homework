### Task 1.2
### Write a Python program to count the number of characters (character frequency) in a string (ignore case of letters).


def count_characters(input_string):
    frequency_dict = {}
    for char in input_string.lower():
        frequency_dict[char] = frequency_dict.get(char, 0) + 1
    return frequency_dict


# =============================================================================
# test_string = "Oh, it is python"
# print(count_characters(test_string))
# =============================================================================
