import asyncio
import threading
from abc import ABC, abstractmethod
from typing import List
import Data
from Data import add_test_form, parse_test_condition
from Database import Database
from EdgeGetter import getEdges
from Engine.Users import User
from Form import formToJSON
from NotificationHandler import send_notification_by_id, send_questionnaire
from user_lists import get_role, take_test

questionnaires = {}
testNodes = {}
decisionNodes = {}
stringNodes = {}
complexNodes = {}


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


def buildNode(dal_node):
    if dal_node.op_code == 1:
        if dal_node.id in questionnaires:
            return questionnaires[dal_node.id]
        questionnaires[dal_node.id] = Questionnaire(dal_node.id, dal_node.title, formToJSON(dal_node.form),
                                                    dal_node.form_id)
        return questionnaires[dal_node.id]
    elif dal_node.op_code == 2:
        if dal_node.id in testNodes:
            return testNodes[dal_node.id]
        testNodes[dal_node.id] = TestNode(dal_node.id, dal_node.title, dal_node.tests, dal_node.in_charge)
        return testNodes[dal_node.id]
    elif dal_node.op_code == 4:
        if dal_node.id in stringNodes:
            return stringNodes[dal_node.id]
        stringNodes[dal_node.id] = StringNode(dal_node.id, dal_node.title, dal_node.text, dal_node.actors)
        return stringNodes[dal_node.id]
    elif dal_node.op_code == 6:
        if dal_node.id in complexNodes:
            return complexNodes[dal_node.id]
        flow = buildNode(dal_node.flow)
        complexNodes[dal_node.id] = ComplexNode(dal_node.id, dal_node.title, flow)
        return complexNodes[dal_node.id]


async def end_test(node, participants):
    if len(node.edges) == 0:
        for participant in participants:
            await send_notification_by_id(participant.id, {'type': 'terminate'})


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
        self.edges = []
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.number = number

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        Database.addNodePosition(participant.id, self.id)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)
        Database.deletePosition(participant.id, self.id, "node")

    async def exec(self) -> None:
        self.edges = getEdges(self.id)
        await self.notify()
        threads = []
        for edge in self.edges:
            threads.append(asyncio.create_task(edge.exec()))
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
            for edge in self.edges:
                edge.attach(participant)
        await end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


class Decision(Node):
    def __init__(self, node_id, title, conditions):
        super(Decision, self).__init__()
        self.id = node_id
        self.title = title
        self.edges = []
        self.conditions = conditions
        self.lock = threading.Lock()
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        Database.addNodePosition(participant.id, self.id)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)
        Database.deletePosition(participant.id, self.id, "node")

    async def exec(self) -> None:
        self.edges = getEdges(self.id)
        await self.notify()
        threads = []
        if self.edges[0].has_actors():
            threads.append(asyncio.create_task(self.edges[0].exec()))
        if self.edges[1].has_actors():
            threads.append(asyncio.create_task(self.edges[1].exec()))
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
                self.edges[0].attach(participant)
            else:
                self.edges[1].attach(participant)

    async def get_results(self, participant):
        for condition in self.conditions:
            if condition['type'].rstrip() == 'trait condition':
                if not (Data.parse_trait_condition(participant, condition['satisfy'], condition['test'])):
                    return False
            elif condition['type'].rstrip() == 'questionnaire condition':
                if not (await Data.parse_questionnaire_condition(participant,
                                                                 condition['questionnaireNumber'],
                                                                 condition['questionNumber'],
                                                                 condition['acceptedAnswers'])):
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
        self.edges = []
        self.lock = threading.Lock()
        self.participants = []
        lower_actors = []
        for actor in actors:
            lower_actors.append(str(actor).lower())
        self.actors = lower_actors

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        Database.addNodePosition(participant.id, self.id)

    def detach(self, participant: User) -> None:
        print("detaching")
        self.participants.remove(participant)
        Database.deletePosition(participant.id, self.id, "node")

    async def exec(self) -> None:
        self.edges = getEdges(self.id)
        await self.notify()
        threads = []
        for edge in self.edges:
            threads.append(asyncio.create_task(edge.exec()))
        for t in threads:
            await t

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            if self.actors.__contains__(participant.role):
                await send_notification_by_id(participant.id, {'type': 'notification', 'text': self.text})
            for edge in self.edges:
                edge.attach(participant)
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
        self.edges = []
        self.lock = threading.Lock()
        self.participants: List[User] = []

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        Database.addNodePosition(participant.id, self.id)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)
        Database.deletePosition(participant.id, self.id, "node")

    async def exec(self) -> None:
        self.edges = getEdges(self.id)
        await self.notify()
        threads = []
        for edge in self.edges:
            threads.append(asyncio.create_task(edge.exec()))
        for t in threads:
            await t

    async def notify(self) -> None:
        self.lock.acquire()
        participants2 = self.participants.copy()
        self.participants = []
        self.lock.release()
        for participant in participants2:
            for test in self.tests:
                await take_test(participant.id, test, self.in_charge)
                add_test_form(test.name, participant)
            for edge in self.edges:
                edge.attach(participant)
        await end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0


class ComplexNode(Node):
    def __init__(self, node_id, title, flow):
        super(ComplexNode, self).__init__()
        self.id = node_id
        self.title = title
        self.edges = []
        self.lock = threading.Lock()
        self.participants: List[User] = []
        self.flow = flow

    def attach(self, participant: User) -> None:
        self.participants.append(participant)
        Database.addNodePosition(participant.id, self.id)

    def detach(self, participant: User) -> None:
        self.participants.remove(participant)
        Database.deletePosition(participant.id, self.id, "node")

    async def exec(self) -> None:
        self.edges = getEdges(self.id)
        await self.notify()
        threads = []
        for edge in self.edges:
            threads.append(asyncio.create_task(edge.exec()))
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
            for edge in self.edges:
                edge.attach(participant)
        for t in threads:
            await t
        await end_test(self, participants2)

    def has_actors(self):
        return len(self.participants) != 0
