# Task 7.1
# Implement class-based context manager for opening and working with file,
# including handling exceptions. Do not use 'with open()'.
# Pass filename and mode via constructor.


class File:
    """
    Context manager for opening and working with files,
    including handling exceptions.

    INIT
        filename - Type string. Filename with/without filepath.
        mode - Type string. Mode for opening filename.

    ATTRIBUTES
        file - file object

    """

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"Starting operation on file '{self.filename}'...")
        try:
            self.file = open(self.filename, self.mode)
        except Exception as err:
            print(f"Exception: {err.__class__.__name__} - {err}")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception: {exc_type} - {exc_value}\n")
        else:
            print("Operation finished successfully\n")
        if self.file:
            self.file.close()
        return True


# =============================================================================
# with File("text.txt", "w") as f:
#     f.write("Hello, world")
# with File("text.txt", "r") as f:
#     f.write("Hello, world")
# with File("text2.txt", "r") as f:
#     f.read()
# =============================================================================
