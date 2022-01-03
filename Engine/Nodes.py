import json
import threading
import time
from _thread import start_new_thread
from abc import ABC, abstractmethod
from typing import List
from Data import add_questionnaire, add_test
from Engine.Users import User, answer_questionnaire, take_test
from user_lists import get_role


class Node(ABC):
    def __init__(self):
        self.min_time = None
        self.max_time = None

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


def set_time(node, min_time, max_time):
    print(2)
    node.min_time = min_time
    node.max_time = max_time


class Questionnaire(Node):
    def __init__(self, node_id, title, duration, form, number):
        super(Questionnaire, self).__init__()
        self.id = node_id
        self.title = title
        self.duration = duration
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
        i=0
        for next_node in self.next_nodes:
            if i==len(self.next_nodes)-1:
                next_node.exec()
            else:
                start_new_thread(next_node.exec, ())
            i+=1

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            if self.min_time is not None:
                time.sleep(self.min_time)
            # send questionnaire to participant
            answers = answer_questionnaire(self.form, participant.socket)
            answers.update({'questionnaire_number': self.number})
            time.sleep(int(self.duration))
            add_questionnaire(answers, participant)
            for next_node in self.next_nodes:
                next_node.attach(participant)
        end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


class Decision(Node):
    def __init__(self, node_id, title, conditions):
        super(Decision, self).__init__()
        self.id = node_id
        self.title = title
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
        for participant in participants2:
            if self.min_time is not None:
                time.sleep(self.min_time)
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
        super(StringNode, self).__init__()
        self.id = node_id
        self.title = title
        self.text = text
        self.next_nodes = []
        self.lock = threading.Lock()
        self.participants = []
        lower_actors = []
        for actor in actors:
            lower_actors.append(str(actor).lower())
        self.actors = lower_actors

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        i=0
        for next_node in self.next_nodes:
            if i == len(self.next_nodes) - 1:
                next_node.exec()
            else:
                start_new_thread(next_node.exec, ())
            i += 1

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            print(participant.role)
            if self.min_time is not None:
                time.sleep(self.min_time)
            if self.actors.__contains__(participant.role):
                participant.socket.send((json.dumps({'type': 'notification', 'text': self.text})+'$').encode('ascii'))
            for next_node in self.next_nodes:
                next_node.attach(participant)
        for role in self.actors:
            r = get_role(role)
            if r is not None:
                r.socket.send((json.dumps({'type': 'notification', 'text': self.text})+'$').encode('ascii'))
        # end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


class TestNode(Node):
    def __init__(self, node_id, title, tests, in_charge):
        super(TestNode, self).__init__()
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
        i = 0
        for next_node in self.next_nodes:
            if i == len(self.next_nodes) - 1:
                next_node.exec()
            else:
                start_new_thread(next_node.exec, ())
            i += 1

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            if self.min_time is not None:
                time.sleep(self.min_time)
            remaining = self.max_time - self.min_time
            for test in self.tests:
                results = take_test(participant.id, test, remaining, self.in_charge, participant.socket)
                if results is None:
                    print("come back tomorrow")
                    break
                add_test(test.name, results, participant)
                remaining -= test.duration
                if remaining <= 0:
                    print("tests timing doesn't make sense")
            for next_node in self.next_nodes:
                next_node.attach(participant)
        end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


class TimeNode(Node):
    def __init__(self, node_id, min_time, max_time):
        super(TimeNode, self).__init__()
        self.id = node_id
        self.min_time = min_time
        self.max_time = max_time
        self.lock = threading.Lock()
        self.next_nodes = []
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def exec(self) -> None:
        self.notify()
        i = 0
        for next_node in self.next_nodes:
            if i == len(self.next_nodes) - 1:
                next_node.exec()
            else:
                start_new_thread(next_node.exec, ())
            i += 1

    def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            for next_node in self.next_nodes:
                next_node.attach(participant)
        end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0
