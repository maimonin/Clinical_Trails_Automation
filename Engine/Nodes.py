import json
import threading
from abc import ABC, abstractmethod
from typing import List

from Data import add_questionnaire
from Engine.Users import User, get_role, answer_questionnaire
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
        print("Questionnaire: Attached an observer.")
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
            log("participant " + participant.id + " in data questionnaire with title: " + self.title)
            # send questionnaire to participant
            answers = answer_questionnaire(participant, self.form, participant.socket)
            add_questionnaire(answers, participant)
            self.next.attach(participant)
        else:
            actor = get_role(self.role)
            # ask server to send request to actors and receive answers
            results = actor.update(lambda: print("I'm a "+self.role))
            add_questionnaire(results, participant)
            self.next.attach(participant)

    def has_actors(self):
        return len(self.participants) != 0


class Decision(Node):
    def __init__(self, node_id, title, actors, form, next_options, condition):
        self.id = node_id
        self.title = title
        self.form = form
        self.actors = actors
        self.next_list = next_options
        self.condition = condition
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
            #log("participant id" + participant.id + "in decision node with title: " + self.title)
            self.detach(participant)
            if self.condition(participant):
                self.next_list[0].attach(participant)
            else:
                self.next_list[1].attach(participant)


class StringNode(Node):
    def __init__(self, node_id, title, actors, text, next_node):
        self.id = node_id
        self.title = title
        self.actors = actors
        self.text = text
        self.next = next_node

    participants: List[User] = []

    def attach(self, participant: User) -> None:
        print("String node: Attached an observer.")
        self.participants.append(participant)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    def notify(self) -> None:
        print("String node: Notifying observers...")
        for participant in self.participants:
            #log("participant id" + participant.id + "in string node with title: " + self.title)
            #Server.send_feedback(participant.socket, self.text)
            self.detach(participant)