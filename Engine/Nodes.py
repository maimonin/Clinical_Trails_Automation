from abc import ABC, abstractmethod
from typing import List
from Engine import Data, Server
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


class DataEntering(Node):
    def __init__(self, role, next_node):
        global node_id
        self.id = node_id
        self.role = role
        self.next = next_node
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
        print("Hello: Notifying observers...")
        for participant in self.participants:
            if self.role == "participant":
                # ask server to send request to actors and receive answers
                results = participant.update(lambda: print("I'm a participant"))
                Data.add_data(results, participant)
                self.detach(participant)
                self.next.attach(participant)
            else:
                actor = Server.get_role(self.role)
                # ask server to send request to actors and receive answers
                results = actor.update(lambda: print("I'm a "+self.role))
                Data.add_data(results, participant)
                self.detach(participant)
                self.next.attach(participant)


class Decision(Node):
    def __init__(self, role, next_options, condition):
        global node_id
        self.id = node_id
        self.role = role
        self.nexts = next_options
        self.condition = condition
        node_id += 1

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        print("Decision: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        if condition():
            self.nexts[0].exec()
        else:
            self.next[1].exec()

    def notify(self) -> None:
        print("Decision: Notifying observers...")
        for participant in self.participants:
            if self.role == "participant":
                # ask server to send request to actors and receive answers
                results = participant.update(lambda: print("I'm a participant"))
                Data.add_data(results, participant)
                self.detach(participant)
                self.next.attach(participant)
            else:
                actor = Server.get_role(self.role)
                # ask server to send request to actors and receive answers
                results = actor.update(lambda: print("I'm a "+self.role))
                Data.add_data(results, participant)
                self.detach(participant)
                self.next.attach(participant)