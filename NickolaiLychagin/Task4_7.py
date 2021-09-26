# Task 4.7
# Implement a class Money to represent value and currency. You need to
# implement methods to use all basic arithmetics expressions (comparison,
# division, multiplication, addition and subtraction). Tip: use class
# attribute exchange rate which is dictionary and stores information
# about exchange rates to your default currency.

from functools import total_ordering


@total_ordering
class Money:
    """
    Money class.

    INIT
        value - Type float.
        currency - Type string. Default to 'USD'.

    ATTRIBUTES
        RATES - Type dictionary. Exchange rates of all currencies to USD.   
        __rates - Type dictionary. Initialized money value in all currencies.
        
    METHODS
        Comparison, division, multiplication, addition and subtraction of instances.

    """

    RATES = {"USD": 1, "EUR": 0.853627, "BYN": 2.503, "JPY": 110.790480}

    def __init__(self, value, currency="USD"):
        self.__value = value
        self.__currency = currency
        self.__rates = {
            k: self.__value / Money.RATES[self.__currency] * v
            for k, v in Money.RATES.items()
        }

    def __repr__(self):
        return f"{round(self.__value, 2):.2f} {self.__currency}"

    def __add__(self, other):
        value = self.__value + other.__rates[self.__currency]
        return Money(value, self.__currency)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        value = self.__value - other.__rates[self.__currency]
        return Money(value, self.__currency)

    def __mul__(self, other):
        if (isinstance(other, int) or isinstance(other, float)) and other >= 0:
            return Money(self.__value * other, self.__currency)
        else:
            raise Exception(
                "Money can be multiplied only by zero or positive integer or float"
            )

    def __rmul__(self, other):
        if (isinstance(other, int) or isinstance(other, float)) and other >= 0:
            return Money(self.__value * other, self.__currency)
        else:
            raise Exception(
                "Money can be multiplied only by zero or positive integer or float"
            )

    def __truediv__(self, other):
        if (isinstance(other, int) or isinstance(other, float)) and other > 0:
            return Money(self.__value / other, self.__currency)
        else:
            raise Exception("Money can be divided only by positive integer or float")

    def __eq__(self, other):
        return self.__value == other.__rates[self.__currency]

    def __gt__(self, other):
        return self.__value > other.__rates[self.__currency]


# =============================================================================
# x = Money(10, "BYN")
# y = Money(11) # define your own default value, e.g. “USD”
# z = Money(12.34, "EUR")
# print(z + 3.11 * x + y * 0.8) # result in “EUR”
# lst = [Money(10,"BYN"), Money(11), Money(12.01, "JPY")]
# s = sum(lst)
# print(s)
# =============================================================================
