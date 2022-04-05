import asyncio
import datetime
import json
import socket
from _thread import *
import threading
import Data
import Nodes
from Database import Database
from EdgeGetter import edges, buildEdge
from Edges import NormalEdge, RelativeTimeEdge, FixedTimeEdge
from Engine.Nodes import Questionnaire, TestNode, Decision, StringNode, set_time, ComplexNode
from Form import buildFromJSON
from Logger import log
import user_lists
from Test import Test

OP_NODE_QUESTIONNAIRE = 1
OP_NODE_DATA_ENTRY = 2
OP_NODE_DECISION = 3
OP_NODE_STRING = 4
OP_NODE_TIME = 5
OP_NODE_COMPLEX = 6


def get_data(s):
    data = ""
    curr = s.recv(1)
    curr = curr.decode()
    while curr != "$":
        data += curr
        curr = s.recv(1)
        curr = curr.decode()
    return data


def parse_Questionnaire(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = Questionnaire(node_dict['id'], node_details['title'], content['questions'],
                         content['questionnaire_number'])
    form = buildFromJSON(content)
    Database.addNode(node, node_dict['op_code'])
    Database.addForm(form)
    Database.addQuestionnaire(node.id, form.questionnaire_number, node)
    Nodes.questionnaires[node.id] = node
    return node


def parse_Test(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    tests = []
    for test_data in content['tests']:
        test = Test(test_data['name'], test_data['duration'], test_data['instructions'], test_data['staff'])
        tests.append(test)
        staff = ', '.join(test.staff)
        Database.addTest(node_dict['id'], test.name, test.instructions, staff, test.duration)
    node = TestNode(node_dict['id'], node_details['title'], tests, node_details['actor in charge'])
    Database.addNode(node, node_dict['op_code'])
    Database.addTestNode(node)
    Nodes.testNodes[node.id] = node
    return node


def parse_Decision(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    conditions = content['condition']
    node = Decision(node_dict['id'], node_details['title'], conditions)
    Database.addNode(node, node_dict['op_code'])
    for condition in conditions:
        if condition['type'] == "questionnaire condition":
            Database.addQuestionnaireCond(
                node.id, condition['title'], condition['questionnaireNumber'],
                condition['questionNumber'], str(condition['acceptedAnswers'])
            )
        elif condition['type'] == "test condition":
            Database.addTestCond(
                node.id, condition['title'], condition['test'],
                condition['satisfy']['type'],
                condition['satisfy']['value']
            )
        elif condition['type'] == "trait condition":
            Database.addTraitCond(
                node.id, condition['title'], condition['test'],
                condition['satisfy']['type'],
                condition['satisfy']['value']['min'],
                condition['satisfy']['value']['max']
            )

    return node


def parse_String_Node(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = StringNode(node_dict['id'], node_dict['title'], content['text'], node_details['actors'])
    Database.addNode(node, node_dict['op_code'])
    Database.addStringNode(node.id, content['text'])
    for actor in node_details['actors']:
        Database.addActorToNotify(node.id, actor)
    Nodes.stringNodes[node.id] = node
    return node


def parse_Complex_Node(node_dict):
    content = node_dict['content']
    flow = new_workflow(content['flow'])
    node = ComplexNode(node_dict['id'], node_dict['title'], flow)
    # add complex node to nodes and complex nodes
    # add flow to workflows
    Database.addNode(node, node_dict["op_code"])
    Database.addComplexNode(node.id, flow.id)
    Nodes.complexNodes[node.id] = node
    return node


def add_times(time_node, other_node):
    set_time(other_node, time_node.min_time, time_node.max_time)


async def register_user(user_dict):
    user = user_lists.add_user(user_dict['role'], user_dict['sex'], user_dict['age'], user_dict['id'])
    if user.role == "participant":
        workflow = Database.getWorkflow(user_dict['workflow'])
        if workflow is None:
            print("No workflow yet")
            Database.addParticipant(user_dict['id'], user_dict['name'], user_dict['sex'], user_dict['age'],
                                    user_dict['workflow'])
        else:
            Database.addParticipant(user_dict['id'], user_dict['name'], user_dict['sex'],
                                    user_dict['age'], user_dict['workflow'])
            # start participant's workflow from start node
            dalStart = Database.getNode(workflow[1])
            start = Nodes.buildNode(dalStart)
            start.attach(user)
            await start.exec()
    else:
        Database.addStaff(user_dict['id'], user_dict['name'], user_dict['role'],
                          user_dict['sex'], user_dict['age'], "yes")


async def load_user(user_id):
    user = Database.getUser(user_id)
    dal_current_positions = Database.getCurrentPositions(user.id)
    for current in dal_current_positions:
        if current[0] == "edge":
            edge = buildEdge(current[1])
            edge.attach(user)
            asyncio.create_task(edge.exec())
        else:
            node = Nodes.buildNode(current[1])
            node.attach(user)
            asyncio.create_task(node.exec())


def new_workflow(data_dict):
    nodes = {}
    outputs = {}
    inputs = {}
    for node in data_dict['nodes']:
        if node['op_code'] == OP_NODE_QUESTIONNAIRE:
            nodes[node['id']] = parse_Questionnaire(node)
        elif node['op_code'] == OP_NODE_DATA_ENTRY:
            nodes[node['id']] = parse_Test(node)
        elif node['op_code'] == OP_NODE_DECISION:
            nodes[node['id']] = parse_Decision(node)
        elif node['op_code'] == OP_NODE_STRING:
            nodes[node['id']] = parse_String_Node(node)
        elif node['op_code'] == OP_NODE_COMPLEX:
            nodes[node['id']] = parse_Complex_Node(node)
        for out in node['outputs']:
            outputs[out['id']] = node['id']
        for inp in node['inputs']:
            inputs[inp['id']] = node['id']
    first_node = data_dict['nodes'][0]['id']
    for edge in data_dict['edges']:
        first_id = outputs[edge['start']]
        second_id = inputs[edge['end']]
        if edge['type'] == 0:
            e = NormalEdge(edge['id'])
            edges[e.id] = e
            Database.addEdge(e.id, first_id, second_id, None, None, None, None)
        elif edge['type'] == 1:
            min_json = edge['content']['min']
            min_time = int(min_json['seconds']) + (60 * int(min_json['minutes'])) + (360 * int(min_json['hours']))
            max_json = edge['content']['max']
            max_time = int(max_json['seconds']) + (60 * int(max_json['minutes'])) + (360 * int(max_json['hours']))
            e = RelativeTimeEdge(edge['id'], min_time, max_time)
            edges[e.id] = e
            Database.addEdge(e.id, first_id, second_id, min_time, max_time, None, None)
        elif edge['type'] == 2:
            min_time = datetime.datetime.strptime(edge['content']['min'], '%d/%m/%y %H:%M:%S')
            max_time = datetime.datetime.strptime(edge['content']['max'], '%d/%m/%y %H:%M:%S')
            e = FixedTimeEdge(edge['id'], min_time, max_time)
            edges[e.id] = e
            Database.addEdge(e.id, first_id, second_id, None, None, min_time, max_time)

    Database.addWorkflow(data_dict["id"], first_node)
    log("created workflow")
    return nodes[first_node]


def load_workflow(workflow_id):
    Database.getWorkflow(workflow_id)


def parser_init():
    global workflows
    global print_lock
    workflows = {}
    print_lock = threading.Lock()

