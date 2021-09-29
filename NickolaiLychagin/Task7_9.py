# Task 7.9
# Implement an iterator class EvenRange, which accepts start and end
# of the interval as an init arguments and gives only even numbers
# during iteration. If user tries to iterate after it gave all possible
# numbers Out of numbers! should be printed.
# Note: Do not use function range() at all.


class EvenRange:
    """
    Custom iterator over even numbers between start(including)
    and end(excluding).

    INIT
        start - Type int. Start of interval.
        end - Type int. End of interval.

    METHODS
        __iter__, __next__ - iterate over even numbers in the interval.
    """

    def __init__(self, start, end):
        if isinstance(start, int) and isinstance(end, int):
            if start < end:
                self.__start = start - 2 if start % 2 == 0 else start - 1
                self.__end = end - 2 if end % 2 == 0 else end - 1
                self.__iterstate = False
            else:
                raise ValueError("Start must be less than end!")
        else:
            raise TypeError("Start or end is not a number!")

    def __iter__(self):
        self.__iterstate = True
        return self

    def __next__(self):
        if self.__start < self.__end:
            self.__start += 2
            return self.__start
        if self.__iterstate:                
            print("'Out of numbers!'")
            raise StopIteration                   
        return "'Out of numbers!'"
        
# =============================================================================
# er1 = EvenRange(7,11)
# print(next(er1))
# print(next(er1))
# print(next(er1))
# print(next(er1))
# er2 = EvenRange(3, 14)
# for number in er2:
#     print(number, end = " ")
# er3 = EvenRange(7,7)
# er3 = EvenRange(7,"8")
# =============================================================================
