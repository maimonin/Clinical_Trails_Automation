import asyncio
import datetime
import threading
from abc import ABC, abstractmethod
from asyncio import sleep
from typing import List
from Database import Database
from NodeGetter import getNode
from Users import User


class Edge(ABC):
    def __init__(self):
        self.next_nodes = []

    @abstractmethod
    def attach(self, observer: User) -> None:
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
        self.min_time = min_time
        self.max_time = max_time
        self.next_node = None
        self.lock = threading.Lock()
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
        Database.addEdgePosition(participant.id, self.id, datetime.datetime.now())
        self.participants.append(participant)

    async def exec(self) -> None:
        self.next_node = getNode(self.id)
        if self.next_node is not None:
            await self.notify()
            await asyncio.create_task(self.next_node.exec())

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            if self.min_time is not None:
                started = datetime.datetime.strptime(
                    Database.getTimeStarted(participant.id, self.id).rpartition('.')[0],
                    '%Y-%m-%d %H:%M:%S')
                sleep_time = (started + datetime.timedelta(seconds=self.min_time)
                              - datetime.datetime.now()).total_seconds()
                if sleep_time > 0:
                    self.next_node.attach(participant)
                    await sleep(sleep_time)
                elif sleep_time < 0 and (self.max_time - self.min_time + sleep_time < 0):
                    print("error node is late")
                else:
                    self.next_node.attach(participant)
                Database.deletePosition(participant.id, self.id, "edge")

    def has_actors(self):
        return len(self.participants) != 0


class FixedTimeEdge(Edge):
    def __init__(self, edge_id, min_time, max_time):
        super(FixedTimeEdge, self).__init__()
        self.id = edge_id
        self.min_time = min_time
        self.max_time = max_time
        self.next_node = None
        self.lock = threading.Lock()
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
        Database.addEdgePosition(participant.id, self.id, datetime.datetime.now())
        self.participants.append(participant)

    async def exec(self) -> None:
        self.next_node = getNode(self.id)
        if self.next_node is not None:
            await self.notify()
            await asyncio.create_task(self.next_node.exec())

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        x = datetime.datetime.now()
        if self.max_time is not None and self.max_time < x:
            print("error node is late")
            return
        if self.min_time is not None and x < self.min_time:
            await sleep((self.min_time - x).total_seconds())
        for participant in participants2:
            self.next_node.attach(participant)
            Database.deletePosition(participant.id, self.id, "edge")

    def has_actors(self):
        return len(self.participants) != 0


class NormalEdge(Edge):
    def __init__(self, edge_id):
        super(NormalEdge, self).__init__()
        self.id = edge_id
        self.next_node = None
        self.lock = threading.Lock()
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
        Database.addEdgePosition(participant.id, self.id, datetime.datetime.now())
        self.participants.append(participant)

    async def exec(self) -> None:
        self.next_node = getNode(self.id)
        if self.next_node is not None:
            await self.notify()
            await asyncio.create_task(self.next_node.exec())

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            self.next_node.attach(participant)
            Database.deletePosition(participant.id, self.id, "edge")

    def has_actors(self):
        return len(self.participants) != 0
