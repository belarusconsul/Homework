# Task 7.10
# Implement a generator which will generate odd numbers endlessly.

import sys
import time


def endless_generator():
    """
    Generator which generates odd numbers endlessly.

    Yields
    ------
    odd : TYPE integer
        DESCRIPTION. Odd number starting from 1.

    """
    odd = 1
    while True:
        yield odd
        odd += 2
        sys.stdout.flush()
        time.sleep(1)


# =============================================================================
# gen = endless_generator()
# while True:
#     print(next(gen), end=" ")
# =============================================================================
