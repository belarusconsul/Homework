# Task 7.2
# Implement context manager for opening and working with file,
# including handling exceptions with @contextmanager decorator.

from contextlib import contextmanager, ExitStack


@contextmanager
def open_file(filename, mode):
    """
    Context manager for opening and working with files,
    including handling exceptions.

    Parameters
    ----------
    filename : TYPE string.
        DESCRIPTION. Filename with/without filepath.
    mode : TYPE string.
        DESCRIPTION. Mode for opening filename.

    Yields
    ------
    file : TYPE file object.
        DESCRIPTION. Open filename in mode, after operation on file close it.

    """
    print(f"Starting operation on file '{filename}'...")
    file = None
    stack = ExitStack()
    try:
        stack.enter_context(open(filename, mode))
    except Exception as err:
        print(f"Exception: {err.__class__.__name__} - {err}")
    else:
        file = open(filename, mode)
    with stack:
        try:
            yield file
        except Exception as err:
            print(f"Exception: {err.__class__.__name__} - {err}\n")
        else:
            print("Operation finished successfully\n")
        finally:
            if file:
                file.close()


# =============================================================================
# with open_file("text.txt", "w") as f:
#     f.write("Hello, world")
# with open_file("text.txt", "r") as f:
#     f.write("Hello, world")
# with open_file("text2.txt", "r") as f:
#     f.read()
# =============================================================================
