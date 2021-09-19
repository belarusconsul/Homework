### Task 4.2
### Write a function that check whether a string is a palindrome or not.
### Usage of any reversing functions is prohibited.


def check_palindrome(input_string):
    """
    Check whether a string is a palindrome or not

    Parameters
    ----------
    input_string : TYPE string
        DESCRIPTION : any string

    Returns
    -------
    bool
        DESCRIPTION : True if a string is a palindrome, False - otherwise.

    """

    strip_string = "".join(
        [i.lower() for i in input_string if i.isalpha() or i.isdigit()]
    )
    str_len = len(strip_string)
    for i in range(str_len // 2):
        if strip_string[i] != strip_string[str_len - 1 - i]:
            return False
    return True


# =============================================================================
# test_string = "Eva, can I see bees in a cave?"
# print(check_palindrome(test_string))
# test_string = "Eva, can I see bee in a cave?"
# print(check_palindrome(test_string))
# test_string = "01.02.2010"
# print(check_palindrome(test_string))
# =============================================================================
