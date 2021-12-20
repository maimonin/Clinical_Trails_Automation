import threading
from abc import ABC, abstractmethod
from typing import List
from Engine import Data, Server
from Engine.Server import log
from Engine.User import User

node_id = 0


class Node(ABC):
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


class DataEntering(Node):
    def __init__(self, role, next_node, titly):
        global node_id
        self.id = node_id
        self.title=titly
        self.role = role
        self.next = next_node
        self.lock= threading.Lock()
        node_id += 1

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        print("DataEntering: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        self.next.exec()

    def notify(self) -> None:
        self.lock.acquire()
        participants2=self.participants.copy()
        self.participants=[]
        self.lock.release()
        for participant in participants2:
            log("participant id"+ participant.id + " in data entering node with title: " + self.title)
            if self.role == "participant":
                # ask server to send request to actors and receive answers
                results = participant.update(lambda: print("I'm a participant"))
                Data.add_data(results, participant)
                self.next.attach(participant)
            else:
                actor = Server.get_role(self.role)
                # ask server to send request to actors and receive answers
                results = actor.update(lambda: print("I'm a "+self.role))
                Data.add_data(results, participant)
                self.next.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0

class Decision(Node):
    def __init__(self,next_options, condition, titly):
        global node_id
        self.id = node_id
        self.title=titly
        self.nexts = next_options
        self.condition = condition
        self.lock= threading.Lock()
        node_id += 1

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        print("Decision: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        if self.nexts[0].has_actors():
            self.nexts[0].exec()
        if self.nexts[1].has_actors():
            self.nexts[1].exec()

    def has_actors(self):
        return len(self.participants)==0

    def notify(self) -> None:
        print("Decision: Notifying observers...")
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            log("participant id" + participant.id + "in decision node with title: " + self.title)
            self.detach(participant)
            if self.condition(participant):
                self.nexts[0].attach(participant)
            else:
                self.nexts[1].attach(participant)