from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

    @abstractmethod
    def exec(self) -> None:
        pass


class Hello(Subject):
    id = 0
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print("Hello: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def exec(self) -> None:
        print("Hello: My state has just changed to: done")
        self.notify()

    def notify(self) -> None:
        print("Hello: Notifying observers...")
        for observer in self._observers:
            if observer.role == "doctor":
                observer.update(lambda: print("Hello doc"))
            elif observer.role == "participant":
                observer.update(lambda: print("Hello participant"))


class World(Subject):
    id = 1
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print("World: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def exec(self) -> None:
        print("World: My state has just changed to: done")
        self.notify()

    def notify(self) -> None:
        print("World: Notifying observers...")
        for observer in self._observers:
            if observer.role == "nurse":
                observer.update(lambda: print("World nurse"))
            elif observer.role == "participant":
                observer.update(lambda: print("World participant"))


class Observer:
    def __init__(self, role):
        self.role = role

    def update(self, callback) -> None:
        callback()


if __name__ == "__main__":
    # The client code.

    hello = Hello()
    world = World()

    observer_a = Observer("doctor")
    hello.attach(observer_a)

    observer_b = Observer("nurse")
    world.attach(observer_b)

    observer_c = Observer("participant")
    hello.attach(observer_c)
    world.attach(observer_c)

    hello.exec()
    world.exec()

    world.detach(observer_c)

    world.exec()
