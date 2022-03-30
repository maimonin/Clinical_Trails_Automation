import asyncio
import datetime
import threading
from abc import ABC, abstractmethod
from asyncio import sleep
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
    async def notify(self) -> None:
        pass

    @abstractmethod
    async def exec(self) -> None:
        pass

    @abstractmethod
    def has_actors(self):
        pass


class RelativeTimeEdge(Edge):
    def __init__(self, edge_id, min_time, max_time):
        super(RelativeTimeEdge, self).__init__()
        self.id = edge_id
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.min_time = min_time
        self.max_time = max_time

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    async def exec(self) -> None:
        await self.notify()
        threads = []
        for next_node in self.next_nodes:
            threads.append(asyncio.create_task(next_node.exec()))
        for t in threads:
            await t

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        if self.min_time is not None:
            await sleep(self.min_time)
        for participant in participants2:
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0


class FixedTimeEdge(Edge):
    def __init__(self, edge_id, min_time, max_time):
        super(RelativeTimeEdge, self).__init__()
        self.id = edge_id
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.min_time = min_time
        self.max_time = max_time

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    async def exec(self) -> None:
        await self.notify()
        threads = []
        for next_node in self.next_nodes:
            threads.append(asyncio.create_task(next_node.exec()))
        for t in threads:
            await t

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        x = datetime.datetime.now()
        if self.max_time is not None and self.max_time > x:
            print("error node is late")
            return
        if self.min_time is not None:
            await sleep(self.min_time.total_seconds() - x.total_seconds())
        for participant in participants2:
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0


class NormalEdge(Edge):
    def __init__(self, edge_id):
        super(NormalEdge, self).__init__()
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.id = edge_id

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        print("attached to edge")

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    async def exec(self) -> None:
        print("executing edge")
        await self.notify()
        threads = []
        for next_node in self.next_nodes:
            threads.append(asyncio.create_task(next_node.exec()))
        for t in threads:
            await t

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        print(self.next_nodes)
        for participant in participants2:
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0
