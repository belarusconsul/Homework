# Task 4.4
# Create hierarchy out of birds. Implement 4 classes:

# class Bird with an attribute name and methods fly and walk.
# class FlyingBird with attributes name, ration, and with the same methods.
#   ration must have default value. Implement the method eat which will
#   describe its typical ration.
# class NonFlyingBird with same characteristics but which obviously
#   without attribute fly. Add same "eat" method but with other
#   implementation regarding the swimming bird tastes.
# class SuperBird which can do all of it: walk, fly, swim and eat.
#   But be careful which "eat" method you inherit.

# Implement str() function call for each class.


class Bird:
    """
    Bird class.

    INIT
        name - Type string.

    METHODS
        fly - Print that bird can fly.
        walk - Print that bird can walk.

    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name} bird can walk"

    def fly(self):
        print(f"{self.name} bird can fly")

    def walk(self):
        print(f"{self.name} bird can walk")


class FlyingBird(Bird):
    """
    FlyingBird class.

    INIT
        name - Type string.
        ration - Type string. Default to 'grains'.

    METHODS
        eat - Print that bird eats mostly ration.

    """

    def __init__(self, name, ration="grains"):
        super().__init__(name)
        self.ration = ration

    def __str__(self):
        return f"{self.name} can walk and fly"

    def eat(self):
        print(f"It eats mostly {self.ration}")


class NonFlyingBird(Bird):
    """
    NonFlyingBird class.

    INIT
        name - Type string.
        ration - Type string. Default to 'fish'.

    METHODS
        swim - Print that bird can swim.
        eat - Print that bird eats mostly ration.
        fly - raise AttributeError.

    """

    def __init__(self, name, ration="fish"):
        super().__init__(name)
        self.ration = ration

    def __str__(self):
        return f"{self.name} can walk and swim"

    def swim(self):
        print(f"{self.name} bird can swim")

    def eat(self):
        print(f"It eats mostly {self.ration}")

    def fly(self):
        raise AttributeError(f"'{self.name}' object has no attribute 'fly'")


class SuperBird(NonFlyingBird, FlyingBird):
    """
    SuperBird class.

    INIT
        name - Type string.
        ration - Type string. Default to 'fish'.

    METHODS
        fly - Use FlyingBird fly method.
        eat - Print that bird eats ration.
    """

    def __init__(self, name, ration="fish"):
        super().__init__(name, ration)

    def __str__(self):
        return f"{self.name} bird can walk, swim and fly"

    def fly(self):
        FlyingBird.fly(self)
        
    def eat(self):
        print(f"It eats {self.ration}")



# =============================================================================
# b = Bird("Any")
# b.walk()
# p = NonFlyingBird("Penguin", "fish")
# p.swim()
# p.fly()
# p.eat()
# c = FlyingBird("Canary")
# str(c)
# c.eat()
# s = SuperBird("Gull")
# str(s)
# s.eat()
# s.fly()
# =============================================================================
