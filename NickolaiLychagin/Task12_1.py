# Task 12.1
# Implement the [dining philosophers problem](https://en.wikipedia.org/wiki/Dining_DATA_problem).

from threading import Thread, Lock
from time import sleep


class Fork:
    """
    Class to represent a fork in the dining philosophers problem.

    ATTRIBUTES:
        fork - a threading Lock object
    """

    def __init__(self):
        self.fork = Lock()


class Philosopher(Thread):
    """
    Class to represent a philosopher in the dining philosophers problem.

    ATTRIBUTES:
        name - philosopher's name
        left - philosopher's left fork
        right - philosopher's right fork
        times - number of times philosopher ate

    METHODS:
        think - philosopher is thinking
        eat - philosopher is eating
        decide - decide whether philosopher should think or eat
        run - start philosopher instance in a separate thread
    """

    def __init__(self, name, left, right):
        Thread.__init__(self)
        self.name = name
        self.left = left
        self.right = right
        self.times = 0

    def think(self):
        print(f"{self.name} is thinking")
        sleep(3)

    def eat(self):
        ending = "time" if self.times == 1 else "times"
        print(f"{self.name} started eating")
        sleep(10)
        self.times += 1
        print(f"{self.name} ate {self.times} {ending}")

    def decide(self):
        while True:
            self.think()
            if not self.left.fork.locked():
                with self.left.fork:
                    print(f"{self.name} took left fork")
                    self.think()
                    if not self.right.fork.locked():
                        with self.right.fork:
                            print(f"{self.name} took right fork")
                            self.eat()

    def run(self):
        self.decide()


if __name__ == '__main__':
    thinkers_list = ["Aristotle", "Socrates", "Plato", "Confucius", "Sartre"]
    forks = [Fork() for i in range(5)]
    philosophers = [Philosopher(f"{thinkers_list[i]}", forks[i], forks[(i+1) % 5]) for i in range(5)]
    for philosopher in philosophers:
        philosopher.start()
