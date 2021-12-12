from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        print("Subject: Notifying observers...")
        _state = 1
        for observer in self._observers:
            observer.update(self)

    @abstractmethod
    def exec(self) -> None:
        pass


class Hello(Subject):
    _state: int = 0
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print("Hello: Attached an observer.")
        self._observers.append(observer)

    def exec(self) -> None:
        print("\nHello")
        print("Subject: My state has just changed to: done")
        self.notify()


class World(Subject):
    _state: int = 0
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print("World: Attached an observer.")
        self._observers.append(observer)

    def exec(self) -> None:
        print("\nWorld")
        print("Subject: My state has just changed to: done")
        self.notify()


class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass


class ConcreteObserver(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state <= 1:
            print("ConcreteObserver: Reacted to the event")


if __name__ == "__main__":
    # The client code.

    hello = Hello()
    world = World()

    observer_a = ConcreteObserver()
    hello.attach(observer_a)

    observer_b = ConcreteObserver()
    world.attach(observer_b)

    observer_c = ConcreteObserver()
    hello.attach(observer_c)
    world.attach(observer_c)

    hello.exec()
    world.exec()

    world.detach(observer_c)

    world.exec()
