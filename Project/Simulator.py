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
            observer.update(react_to_hello)


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
            observer.update(react_to_world)


class Observer:
    def update(self, callback) -> None:
        callback()


def react_to_hello():
    print("hello")


def react_to_world():
    print("world")


if __name__ == "__main__":
    # The client code.

    hello = Hello()
    world = World()

    observer_a = Observer()
    hello.attach(observer_a)

    observer_b = Observer()
    world.attach(observer_b)

    observer_c = Observer()
    hello.attach(observer_c)
    world.attach(observer_c)

    hello.exec()
    world.exec()

    world.detach(observer_c)

    world.exec()
