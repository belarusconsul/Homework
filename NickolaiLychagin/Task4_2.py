# Task 4.2
# Implement custom dictionary that will memorize 10 latest changed keys.
# Using method "get_history" return this keys.


class HistoryDict:
    """
    HistoryDict class.

    INIT
        mydict - Type dictionary. Default to {}.

    ATTRIBUTES
       __memo - Type list. Default to []. Keeps last 10 changed keys in mydict.

    METHODS
        set_value(key, value) - If key not in mydict, insert it, otherwise update it.
                                If key is new or key has been changed,
                                move it to the end of __memo.
        get_history - Return __memo.

    """

    def __init__(self, mydict={}):
        self.__mydict = mydict
        self.__memo = []

    def set_value(self, key, value):
        if key in self.__memo:
            if self.__mydict[key] != value:
                self.__memo.remove(key)
                self.__memo.append(key)
        else:
            self.__memo.append(key)
        if len(self.__memo) > 10:
            del self.__memo[0]
        self.__mydict[key] = value

    def get_history(self):
        return self.__memo


# =============================================================================
# d = HistoryDict({"foo": 42})
# d.set_value("bar", 43)
# print(d.get_history())
# d.set_value(1, 43)
# d.set_value(2, 43)
# d.set_value(3, 43)
# d.set_value(4, 43)
# d.set_value(5, 43)
# d.set_value(6, 43)
# d.set_value(7, 43)
# d.set_value(8, 43)
# d.set_value(9, 43)
# print(d.get_history())
# d.set_value("bar", 43)
# print(d.get_history())
# d.set_value("bar", 44)
# print(d.get_history())
# =============================================================================
