from abc import ABC, abstractmethod
from typing import List

from Engine.User import User


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: User) -> None:
        pass

    @abstractmethod
    def detach(self, observer: User) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

    @abstractmethod
    def exec(self) -> None:
        pass


class Hello(Subject):
    id = 0
    _observers: List[User] = []

    def attach(self, observer: User) -> None:
        print("Hello: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: User) -> None:
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
    _observers: List[User] = []

    def attach(self, observer: User) -> None:
        print("World: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: User) -> None:
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