# Task 7.6
# Create console program for proving Goldbach's conjecture.
# Program accepts number for input and print result. For pressing 'q'
# program succesfully close. Use function from Task 5.5 for validating
# input, handle all exceptions and print user friendly output.

from Task7_5 import *


def check_prime(number):
    """
    Function to check if a number is prime.

    Parameters
    ----------
    number : TYPE integer
        DESCRIPTION. Any integer

    Returns
    -------
    bool
        DESCRIPTION. True if number is prime, False - otherwise

    """
    for i in range(2, number // 2 + 1):
        if (number % i) == 0:
            return False
    return True


def goldbach():
    """
    Function to prove Goldbach's conjecture from user input.
    Function prints to console first prime number combination.

    Returns
    -------
    None.

    """
    while True:
        user_input = input(
            "Please enter an even number greater than 2 or type 'q' to quit\n"
        )
        if user_input == "q":
            break
        try:
            if not check_even(user_input):
                print("Number not even\n")
            else:
                number = int(user_input)
                for i in range(1, number):
                    j = number - i
                    if check_prime(i) and check_prime(j):
                        print(f"{number} = {i} + {j}\n")
                        break
        except Exception as err:
            print(f"{err.__class__.__name__} - {err}\n")


if __name__ == "__main__":
    goldbach()
