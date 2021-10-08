# Optional
# Try different synchronization primitives and fix deadlock in [dining philosophers problem]
# (https://en.wikipedia.org/wiki/Dining_philosophers_problem).

from threading import Thread, Condition
from time import sleep


class Fork:
    """
    Class to represent a fork in the dining philosophers problem.

    ATTRIBUTES:
        cond - a threading Condition object
        status - fork is available (True) or not (False)

    METHODS
        take_fork - make fork unavailable
        return_fork - make fork available
    """

    def __init__(self):
        self.cond = Condition()
        self.status = True

    def take_fork(self):
        with self.cond:
            while not self.status:
                self.cond.wait()
            self.status = False

    def return_fork(self):
        with self.cond:
            self.status = True
            self.cond.notify()


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
            self.left.take_fork()
            print(f"{self.name} took left fork")
            self.right.take_fork()
            print(f"{self.name} took right fork")
            self.eat()
            self.right.return_fork()
            self.left.return_fork()

    def run(self):
        self.decide()


if __name__ == "__main__":
    thinkers_list = ["Aristotle", "Socrates", "Plato", "Confucius", "Sartre"]
    forks = [Fork() for i in range(5)]
    philosophers = [Philosopher(f"{thinkers_list[i]}", forks[i], forks[(i+1) % 5]) for i in range(5)]
    philosophers[0].start()
    sleep(3)
    for philosopher in philosophers[1:]:
        philosopher.start()