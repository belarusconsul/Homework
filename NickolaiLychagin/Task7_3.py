# Task 7.3
# Implement decorator with context manager support for writing
# execution time to log-file. See contextlib module.


import time
from contextlib import ContextDecorator


class Log(ContextDecorator):
    """
    Decorator with context manager support for writing
    execution time to log-file.

    INIT
        filename - Type string. Log-file filename with/without filepath.
        func_name - Type string. Name of the function.

    """

    def __init__(self, filename, func_name):
        self.func_name = func_name
        self.filename = filename

    def __enter__(self):
        print(f"Starting '{self.func_name}' function...")
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception: {exc_type} - {exc_value}\n")
        else:
            with open(self.filename, "a") as f:
                f.write(
                    f"Execution time of '{self.func_name}': {time.time() - self.start} seconds\n"
                )
            print("Operation finished successfully. Log file updated.\n")
        return True


# =============================================================================
# @Log("execution.log", "dumb_func")
# def dumb_func():
#     for i in range(10000000):
#         pass
# @Log("execution.log", "div_zero")
# def div_zero():
#     return 2/0
# 
# dumb_func()
# div_zero()
# =============================================================================
