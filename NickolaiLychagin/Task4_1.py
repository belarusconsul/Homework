# Task 4.1
# Implement a Counter class which optionally accepts the start value and
# the counter stop value. If the start value is not specified the counter
# should begin with 0. If the stop value is not specified it should be
# counting up infinitely. If the counter reaches the stop value,
# print "Maximal value is reached."
# Implement to methods: "increment" and "get"
# If you are familiar with Exception rising use it to display the "Maximal value is reached." message.


class Counter:
    """
    Counter class.

    INIT
        start - Type integer. Default to 0. Start value.
        stop - Type integer. Default to None (counter counts up infinitely). 
               Stop value.

    METHODS
        increment - Increment counter by 1. If the counter reaches
                    the stop value, Exception is risen.
        get - Return counter current value

    """

    def __init__(self, start=0, stop=None):
        self.__start = start
        self.__stop = stop

    def increment(self):
        if self.__stop is not None and self.__start >= self.__stop:
            raise Exception("Maximal value is reached.")
        self.__start += 1

    def get(self):
        return self.__start


# =============================================================================
# c = Counter(start=42)
# c.increment()
# print(c.get())
# 
# c = Counter()
# c.increment()
# print(c.get())
# c.increment()
# print(c.get())
# 
# c = Counter(start=42, stop=43)
# c.increment()
# print(c.get())
# c.increment()
# print(c.get())
# 
# c = Counter(start=2, stop=1)
# c.increment()
# print(c.get())
# =============================================================================
