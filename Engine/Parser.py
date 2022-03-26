import datetime
import json
import socket
from _thread import *
import threading

import Data
from Database import Database
from Edges import NormalEdge, RelativeTimeEdge
from Engine.Nodes import Questionnaire, TestNode, Decision, StringNode, TimeNode, set_time, ComplexNode
from Form import Form
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
    form = Form(content)
    Database.addForm(form)
    Database.addQuestionnaire(node.id, form.questionnaire_number, node)
    return node


def parse_Test(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    tests = []
    for test_data in content['tests']:
        test = Test(test_data['name'], test_data['duration'], test_data['instructions'], test_data['staff'])
        tests.append(test)
    node = TestNode(node_dict['id'], node_details['title'], tests, node_details['actor in charge'])
    return node


def parse_Decision(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    conditions = content['condition']
    node = Decision(node_dict['id'], node_details['title'], conditions)
    return node


def parse_String_Node(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = StringNode(node_dict['id'], node_dict['title'], content['text'], node_details['actors'])
    return node


def parse_Time_Node(node_dict):
    content = node_dict['content']
    min_time = int(content["Min"]['Seconds']) + 60 * int(content["Min"]['Minutes']) + 3600 * int(
        content["Min"]['Hours'])
    max_time = int(content["Max"]['Seconds']) + 60 * int(content["Max"]['Minutes']) + 3600 * int(
        content["Max"]['Hours'])
    node = TimeNode(node_dict['id'], min_time, max_time)
    return node


def add_times(time_node, other_node):
    print(1)
    set_time(other_node, time_node.min_time, time_node.max_time)


async def register_user(user_dict):
    print('regiater')
    user = user_lists.add_user(user_dict['role'], user_dict['sex'], user_dict['age'], user_dict['id'])
    if user.role == "participant":
        Database.addParticipant(user_dict['id'],
                                user_dict['name'], user_dict['sex'], user_dict['age'], user_dict['workflow'])
        if len(workflows) == 0:
            print("No workflow yet")
        else:
            # start participant's workflow
            workflows[user_dict["workflow"]].attach(user)
            await workflows[user_dict["workflow"]].exec()
    else:
        Database.addStaff(user_dict['name'], user_dict['role'])


def parse_Complex_Node(node_dict):
    content = node_dict['content']
    flow = new_workflow(content['flow'])
    node = ComplexNode(node_dict['id'], flow)
    return node


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
        # elif node['op_code'] == OP_NODE_TIME:
        #    nodes[node['id']] = parse_Time_Node(node)
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
        first = nodes[first_id]
        second = nodes[second_id]
        if edge['type'] == 0:
            e = NormalEdge(edge['id'])
            first.next_nodes.append(e)
            e.next_nodes.append(second)
        elif edge['type'] == 1:
            min_json = edge['content']['Min']
            min_time = int(min_json['Seconds']) + (60 * int(min_json['Minutes'])) + (360 * int(min_json['Hours']))
            max_json = edge['content']['max']
            max_time = int(max_json['Seconds']) + (60 * int(max_json['Minutes'])) + (360 * int(max_json['Hours']))
            e = RelativeTimeEdge(edge['id'], min_time, max_time)
            first.next_nodes.append(e)
            e.next_nodes.append(second)
        elif edge['type'] == 2:
            min_time = datetime.strptime(edge['content']['Min'], '%d/%m/%y %H:%M:%S')
            max_time = datetime.strptime(edge['content']['max'], '%d/%m/%y %H:%M:%S')
            e = RelativeTimeEdge(edge['id'], min_time, max_time)
            first.next_nodes.append(e)
            e.next_nodes.append(second)

    Database.addWorkflow(data_dict["id"], "name")
    log("created workflow")
    return nodes[first_node]


def threaded(c):
    print('conn')
    global workflows
    while True:
        data = get_data(c)
        if not data:
            print('Bye')
            break
        data_dict = json.loads(data)
        if data_dict['sender'] == 'simulator':
            register_user(data_dict, c)
            break
        else:
            workflows[data_dict["workflow_id"]] = new_workflow(data_dict)
            break


def send_feedback(user_socket, text):
    user_socket.send((text + '$').encode('ascii'))


def parser_init():
    global workflows
    global print_lock
    workflows = {}
    print_lock = threading.Lock()


def Main():
    open('Logger.txt', 'w').close()
    user_lists.init()
    Data.init()
    Database.init_tables()
    host = ""
    port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    # put the socket into listening mode
    s.listen(5)

    while True:
        c, addr = s.accept()
        start_new_thread(threaded, (c,))


if __name__ == '__main__':
    Main()
