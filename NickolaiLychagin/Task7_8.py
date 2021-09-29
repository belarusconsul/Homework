# Task 7.8
# Implement your custom iterator class called MySquareIterator
# which gives squares of elements of collection it iterates through.


class MySquareIterator:
    """
    Custom iterator over squares of elements in collection.

    INIT
        col - Type list or tuple. List or tuple of integers or floats.

    METHODS
        __iter__, __next__ - iterate over collection
    """

    def __init__(self, col):
        if isinstance(col, (list, tuple)):
            if all(isinstance(i, (int, float)) for i in col):
                self.__col = col
                self.__i = -1
            else:
                raise TypeError("Iterator supports only integers or floats!")
        else:
            raise TypeError("Iterator supports only lists and tuples!")

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.__i += 1
            return self.__col[self.__i] ** 2
        except IndexError:
            raise StopIteration


# =============================================================================
# lst = [1, 2, 3, 4, 5]
# itr = MySquareIterator(lst)
# for item in itr:
#     print(item, end = " ")
# print()
# lst = [1, 2, 3, 4, "5"]
# itr = MySquareIterator(lst)
# lst = {1, 2, 3, 4, 5}
# itr = MySquareIterator(lst)
# =============================================================================
