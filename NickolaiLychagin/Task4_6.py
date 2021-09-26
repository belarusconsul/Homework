# Task 4.6
# A singleton is a class that allows only a single instance of itself
# to be created and gives access to that created instance.
# Implement singleton logic inside your custom class using a method
# to initialize class instance.


class Singleton:
    """
    Singleton class.

    INIT
        decorated - decorated class.

    METHODS
        inst - On the first call, returns the Singleton instance.
               On all subsequent calls, returns the created instance.
    """

    def __init__(self, decorated):
        self.__decorated = decorated

    def __call__(self):
        raise Exception("Singleton class must be initialized through inst method")

    def inst(self):
        try:
            self.__instance
        except AttributeError:
            self.__instance = self.__decorated()
        return self.__instance


@Singleton
class Sun:
    def __init__(self):
        print("Instance created")


# =============================================================================
# p = Sun.inst()
# f = Sun.inst()
# print(p is f)
# s = Sun()
# =============================================================================
