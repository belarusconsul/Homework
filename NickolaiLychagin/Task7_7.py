# Task 7.7
# Implement your custom collection called MyNumberCollection. It should
# be able to contain only numbers. It should NOT inherit any other
# collections. If user tries to add a string or any non numerical object
# there, exception TypeError should be raised. Method init sholud be able
# to take either start,end,step arguments, where start - first number of
# collection, end - last number of collection or some ordered iterable
# collection (see the example). Implement following functionality:

# appending new element to the end of collection
# concatenating collections together using +
# when element is addressed by index(using []), user should get square of the addressed element.
# when iterated using cycle for, elements should be given normally
# user should be able to print whole collection as if it was list.


class MyNumberCollection:
    """
    Custom collection of integers.

    INIT
        a - Two options possible:
            - Type list or tuple. List or tuple of integers.
            - Type integer. Start number in collection.
        b - Type integer. End number in collection. Default to None
        c - Type integer. Step. Default to 1.
        
    ATTRIBUTES:
        __mycol - Type list. List to hold collection.

    METHODS
        append - append new element to the end of collection
        __add__ - concatenate collections together using plus sign
        __getitem__ - when element is addressed by index(using []),
                      get square of the addressed element
        __iter__, __next__ - iterate over collection
        __repr__ - print collection as a list
    """

    @staticmethod
    def __check_int(elem):
        """
        Check that elem is an integer.

        Raises
        ------
        TypeError
            DESCRIPTION. If elem is not an integer.

        Returns
        -------
        None.

        """
        if not isinstance(elem, int):
            raise TypeError(f"'{elem}' - object is not a number!")

    def __init__(self, a, b=None, c=1):
        self.__mycol = []
        self.__i = -1
        if isinstance(a, (list, tuple)):
            if any(not isinstance(elem, int) for elem in a):
                raise TypeError("MyNumberCollection supports only numbers!")
            self.__mycol.extend(a)
        else:
            MyNumberCollection.__check_int(a)
            MyNumberCollection.__check_int(b)
            if a > b:
                raise ValueError("Start number should be less or equal to end number.")
            self.__mycol.extend(range(a, b, c if isinstance(c, int) and c > 1 else 1))
            if b not in self.__mycol:
                self.__mycol.append(b)

    def __repr__(self):
        return "[" + ", ".join([str(elem) for elem in self.__mycol]) + "]"

    def append(self, elem):
        MyNumberCollection.__check_int(elem)
        self.__mycol.append(elem)

    def __add__(self, other):
        return self.__mycol + other.__mycol

    def __getitem__(self, ind):
        MyNumberCollection.__check_int(ind)
        return self.__mycol[ind] ** 2

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.__i += 1
            return self.__mycol[self.__i]
        except IndexError:
            raise StopIteration


# =============================================================================
# col1 = MyNumberCollection(0, 5, 2)
# print(col1)
# col2 = MyNumberCollection((1,2,3,4,5))
# print(col2)
# col3 = MyNumberCollection(1, 5)
# print(col3)
# col3 = MyNumberCollection(5, 1)
# col3 = MyNumberCollection((1,2,3,"4",5))
# col1.append(7)
# print(col1)
# col2.append("string")
# print(col1 + col2)
# print(col1)
# print(col2)
# print(col2[4])
# print(col2["4"])
# for item in col1:
#     print(item, end=" ")
# print()
# col4 = MyNumberCollection((1,2))
# print(next(col4))
# print(next(col4))
# print(next(col4))
# =============================================================================

