import json
import threading
import time
from abc import ABC, abstractmethod
from typing import List
from Data import add_questionnaire, add_test
from Engine.Users import User, answer_questionnaire, take_test, get_role
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


def end_test(node, participants):
    if len(node.next_nodes) == 0:
        for participant in participants:
            participant.socket.send(json.dumps({'type': 'terminate'}).encode('ascii'))


class Questionnaire(Node):
    def __init__(self, node_id, title, form, number):
        self.id = node_id
        self.title = title
        self.form = form
        self.next_nodes = []
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.number = number

    def attach(self, participant: User) -> None:
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
            # send questionnaire to participant
            answers = answer_questionnaire(self.form, participant.socket)
            answers.update({'questionnaire_number': self.number})
            add_questionnaire(answers, participant)
            for next_node in self.next_nodes:
                next_node.attach(participant)
        end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


class Decision(Node):
    def __init__(self, node_id, title, actors, conditions):
        self.id = node_id
        self.title = title
        self.actors = actors
        self.next_nodes = []
        self.conditions = conditions
        self.lock = threading.Lock()
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        if self.next_nodes[0].has_actors():
            self.next_nodes[0].exec()
        if self.next_nodes[1].has_actors():
            self.next_nodes[1].exec()

    def has_actors(self):
        return len(self.participants) != 0

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        print(len(self.conditions))
        for participant in participants2:
            satisfies = True
            for condition in self.conditions:
                if not condition(participant):
                    satisfies = False
            if satisfies:
                self.next_nodes[0].attach(participant)
            else:
                self.next_nodes[1].attach(participant)


class StringNode(Node):
    def __init__(self, node_id, title, text, actors):
        self.id = node_id
        self.title = title
        self.text = text
        self.next_nodes = []
        self.lock = threading.Lock()
        self.actors = actors
        self.participants = []

    def attach(self, participant: User) -> None:
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
            participant.socket.send(json.dumps({'type': 'notification', 'text': self.text}).encode('ascii'))
            for next_node in self.next_nodes:
                next_node.attach(participant)
        for role in self.actors:
            r = get_role(role)
            if r is not None:
                r.socket.send(json.dumps({'type': 'notification', 'text': self.text}).encode('ascii'))
        end_test(self, participants2)

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
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
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
            for test in self.tests:
                results = take_test(participant.id, test, self.in_charge, participant.socket)
                add_test(test['name'], results, participant)
            for next_node in self.next_nodes:
                next_node.attach(participant)
        end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


class TimeNode(Node):
    def __init__(self, node_id, title, sleep_time):
        self.id = node_id
        self.title = title
        self.time = sleep_time
        self.lock = threading.Lock()
        self.next_nodes = []
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
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
        print(participants2)
        for participant in participants2:
            time.sleep(self.time)
            for next_node in self.next_nodes:
                next_node.attach(participant)
        end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0
