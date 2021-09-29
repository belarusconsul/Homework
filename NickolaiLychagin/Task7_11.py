# Task 7.11
# Implement a generator which will geterate Fibonacci numbers endlessly.

import sys
import time


def endless_fib_generator():
    """
    Generator which generates Fibonacci numbers endlessly.

    Yields
    ------
    fib : TYPE integer
        DESCRIPTION. Fibonacci number.

    """
    first = 0
    fib = 1
    while True:
        yield fib
        first, fib = fib, first + fib
        sys.stdout.flush()
        time.sleep(1)


# =============================================================================
# gen = endless_fib_generator()
# while True:
#     print(next(gen), end=" ")
# =============================================================================
