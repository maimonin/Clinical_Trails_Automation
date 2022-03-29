import asyncio
import json
import threading
import time
from _thread import start_new_thread
from abc import ABC, abstractmethod
from typing import List
import Data
from Data import add_questionnaire, add_test, add_test_form, parse_test_condition
from Database import Database
from Engine.Users import User
from NotificationHandler import send_notification_by_id, send_questionnaire
from user_lists import get_role, take_test


class Node(ABC):
    @abstractmethod
    def attach(self, observer: User) -> None:
        pass

    @abstractmethod
    async def detach(self, observer: User) -> None:
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


async def end_test(node, participants):
    if len(node.next_nodes) == 0:
        for participant in participants:
            await send_notification_by_id(participant.id,{'type': 'terminate'})


def set_time(node, min_time, max_time):
    print(2)
    node.min_time = min_time
    node.max_time = max_time


class Questionnaire(Node):
    def __init__(self, node_id, title, form, number):
        super(Questionnaire, self).__init__()
        self.id = node_id
        self.title = title
        self.form = form
        self.next_nodes = []
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.number = number

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        Database.updateNode(participant.id, self.id)

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
        for participant in participants2:
            # send questionnaire to participant
            await send_questionnaire(self.form, self.number, participant.id)
            Data.add_Form(self.number, participant.id)
            for next_node in self.next_nodes:
                next_node.attach(participant)
        await end_test(self, participants2)

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
        Database.updateNode(participant.id, self.id)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)

    async def exec(self) -> None:
        await self.notify()
        threads = []
        if self.next_nodes[0].has_actors():
            threads.append(asyncio.create_task(self.next_nodes[0].exec()))
        if self.next_nodes[1].has_actors():
            threads.append(asyncio.create_task(self.next_nodes[1].exec()))
        for t in threads:
            await t

    def has_actors(self):
        return len(self.participants) != 0

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            if await self.get_results(participant.id):
                self.next_nodes[0].attach(participant)
            else:
                self.next_nodes[1].attach(participant)

    async def get_results(self, participant):
        for condition in self.conditions:
            if condition['type'].rstrip() == 'trait condition':
                if not (Data.parse_trait_condition(participant, condition['satisfy'], condition['test'])):
                    return False
            elif condition['type'].rstrip() == 'questionnaire condition':
                if not (await Data.parse_questionnaire_condition(participant, condition['questionnaireNumber'], condition['questionNumber'], condition['acceptedAnswers'])):
                    return False
            elif condition['type'].rstrip() == 'test condition':
                if not (await parse_test_condition(participant, condition['satisfy'], condition['test'])):
                    return False
        return True


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
        Database.updateNode(participant.id, self.id)

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
        print(self.text)
        for participant in participants2:
            print(participant.id)
            if self.actors.__contains__(participant.role):
                await send_notification_by_id(participant.id, {'type': 'notification', 'text': self.text})
            for next_node in self.next_nodes:
                next_node.attach(participant)
            for role in self.actors:
                r = get_role(role)
                if r is not None:
                    await send_notification_by_id(r.id, {'type': 'notification', 'text': self.text})
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
        Database.updateNode(participant.id, self.id)

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
        print(self.tests)
        for participant in participants2:
            for test in self.tests:
                await take_test(participant.id, test, self.in_charge)
                add_test_form(test.name, participant)
            for next_node in self.next_nodes:
                next_node.attach(participant)
        await end_test(self, participants2)

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
        Database.updateNode(participant.id, self.id)

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


class ComplexNode(Node):
    def __init__(self, node_id, flow):
        super(ComplexNode, self).__init__()
        self.id = node_id
        self.next_nodes = []
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.flow = flow

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        Database.updateNode(participant.id, self.id)

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
        threads = []
        for participant in participants2:
            self.flow.attach(participant)
            threads.append(asyncio.create_task(self.flow.exec()))
            for next_node in self.next_nodes:
                next_node.attach(participant)
        for t in threads:
            await t
        await end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


