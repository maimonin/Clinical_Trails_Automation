import datetime
import threading
import time
from abc import ABC, abstractmethod
from typing import List

from Users import User


class Edge(ABC):
    def __init__(self):
        self.next_nodes = []
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

    @abstractmethod
    def has_actors(self):
        pass


class RelativeTimeEdge(Edge):
    def __init__(self, id, min_time, max_time):
        super(RelativeTimeEdge, self).__init__()
        self.id = id
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.min_time = min_time
        self.max_time = max_time

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        threads = []
        for next_node in self.next_nodes:
            threads.append(threading.Thread(target=next_node.exec, args=()))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        if self.min_time is not None:
            time.sleep(self.min_time)
        for participant in participants2:
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0


class FixedTimeEdge(Edge):
    def __init__(self, id, min_time, max_time):
        super(RelativeTimeEdge, self).__init__()
        self.id = id
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.min_time = min_time
        self.max_time = max_time

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        threads = []
        for next_node in self.next_nodes:
            threads.append(threading.Thread(target=next_node.exec, args=()))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        x = datetime.datetime.now()
        if self.max_time is not None and self.max_time > x:
            print("error node is late")
            return
        if self.min_time is not None:
            time.sleep(self.min_time.total_seconds() - x.total_seconds())
        for participant in participants2:
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0


class NormalEdge(Edge):
    def __init__(self, id):
        super(NormalEdge, self).__init__()
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.id=id

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        threads = []
        for next_node in self.next_nodes:
            threads.append(threading.Thread(target=next_node.exec, args=()))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0
