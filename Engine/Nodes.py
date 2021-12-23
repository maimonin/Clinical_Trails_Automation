import json
import threading
from abc import ABC, abstractmethod
from typing import List

from Data import add_questionnaire, add_test
from Engine.Users import User, get_role, answer_questionnaire, take_test
from Logger import log


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


class Questionnaire(Node):
    def __init__(self, node_id, title, form):
        self.id = node_id
        self.title = title
        self.form = form
        self.next_nodes = []
        self.lock = threading.Lock()

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        log("Questionnaire: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        for next_node in self.next_nodes:
            next_node.exec()

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            log("participant " + str(participant.id) + " in data questionnaire with title: " + self.title)
            # send questionnaire to participant
            answers = answer_questionnaire(self.form, participant.socket)
            add_questionnaire(answers, participant)
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0


class Decision(Node):
    def __init__(self, node_id, title, actors, form, next_options, conditions):
        self.id = node_id
        self.title = title
        self.form = form
        self.actors = actors
        self.next_list = next_options
        self.conditions = conditions
        self.lock = threading.Lock()

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        print("Decision: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        if self.next_list[0].has_actors():
            self.next_list[0].exec()
        if self.next_list[1].has_actors():
            self.next_list[1].exec()

    def has_actors(self):
        return len(self.participants) == 0

    def notify(self) -> None:
        print("Decision: Notifying observers...")
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            log("participant id" + participant.id + "in decision node with title: " + self.title)
            for condition in self.conditions:
                if not condition(participant):
                    self.next_list[1].attach(participant)
            self.next_list[0].attach(participant)


class StringNode(Node):
    def __init__(self, node_id, title, text):
        self.id = node_id
        self.title = title
        self.text = text
        self.next_nodes = []
        self.lock = threading.Lock()

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        log("String node: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        for next_node in self.next_nodes:
            next_node.exec()

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        log("String node: Notifying observers...")
        for participant in participants2:
            log("participant id" + participant.id + "in string node with title: " + self.title)
            participant.socket.send(json.dumps({'type': 'string', 'text': self.text}))

    def has_actors(self):
        return len(self.participants) != 0


class TestNode(Node):
    def __init__(self, node_id, title, tests, in_charge):
        self.id = node_id
        self.title = title
        self.tests = tests
        self.in_charge = in_charge
        self.next_nodes = []
        self.lock = threading.Lock()

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        log("String node: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        for next_node in self.next_nodes:
            next_node.exec()

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        log("String node: Notifying observers...")
        for participant in participants2:
            log("participant " + participant.id + " in test with title: " + self.title)
            for test in self.tests:
                results = take_test(participant.id, test, self.in_charge, participant.socket)
                add_test(test['name'], results, participant)
            for next_node in self.next_nodes:
                next_node.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0
