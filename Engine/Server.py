import json
import socket
from _thread import *
import threading

import Data
from Data import get_test_result
from Engine.Nodes import Questionnaire, TestNode, Decision, StringNode, TimeNode, set_time
from Logger import log
import user_lists
from Test import Test

workflows = {}
print_lock = threading.Lock()
OP_NODE_QUESTIONNAIRE = 1
OP_NODE_DATA_ENTRY = 2
OP_NODE_DECISION = 3
OP_NODE_STRING = 4
OP_NODE_TIME = 5


def parse_Questionnaire(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = Questionnaire(node_dict['id'], node_details['title'], node_details['time'], content['questions'],
                         content['questionnaire_number'])
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


def parse_trait_condition(satisfy, trait):
    if satisfy['type'] == 'range':
        values = satisfy['value']
        return lambda patient: True if values['min'] <= patient.get_traits()[trait] <= values['max'] else False
    else:
        return lambda patient: True if patient.get_traits()[trait] == satisfy['value'] else False


def parse_questionnaire_condition(questionnaire_number, question_number, accepted_answers):
    return lambda patient: Data.check_data(patient, questionnaire_number, question_number, accepted_answers)


def parse_test_condition(satisfy, test_name):
    if satisfy['type'] == 'range':
        values = satisfy['value']
        return lambda patient: True if values['min'] <= int(get_test_result(patient, test_name)) <= values[
            'max'] else False
    else:
        return lambda patient: True if get_test_result(patient, test_name) == satisfy['value'] else False


def parse_Decision(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    conditions = content['condition']
    combined_condition = []
    for condition in conditions:
        if condition['type'].rstrip() == 'trait condition':
            combined_condition.append(parse_trait_condition(condition['satisfy'], condition['test']))
        elif condition['type'].rstrip() == 'questionnaire condition':
            combined_condition.append(
                parse_questionnaire_condition(condition['questionnaireNumber'], condition['questionNumber'],
                                              condition['acceptedAnswers']))
        elif condition['type'].rstrip() == 'test condition':
            combined_condition.append(parse_test_condition(condition['satisfy'], condition['test']))
    node = Decision(node_dict['id'], node_details['title'], combined_condition)
    return node


def parse_String_Node(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = StringNode(node_dict['id'], node_dict['title'], content['text'], node_details['actors'])
    return node


def parse_Time_Node(node_dict):
    content = node_dict['content']
    min_time = int(content["Min"]['Seconds']) + 60*int(content["Min"]['Minutes']) + 3600*int(content["Min"]['Hours'])
    max_time = int(content["Max"]['Seconds']) + 60*int(content["Max"]['Minutes']) + 3600*int(content["Max"]['Hours'])
    node = TimeNode(node_dict['id'], min_time, max_time)
    return node


def add_times(time_node, other_node):
    print(1)
    set_time(other_node, time_node.min_time, time_node.max_time)


def register_user(user_dict, c):
    user = user_lists.add_user(user_dict['role'], user_dict['sex'], user_dict['age'], user_dict['id'], c)
    if user.role == "participant":
        if len(workflows) == 0:
            print("No workflow yet")
            c.close()
        else:
            # start participant's workflow
            workflows[user_dict["workflow"]].attach(user)
            workflows[user_dict["workflow"]].exec()


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
        elif node['op_code'] == OP_NODE_TIME:
            nodes[node['id']] = parse_Time_Node(node)
        for out in node['outputs']:
            outputs[out['id']] = node['id']
        for inp in node['inputs']:
            inputs[inp['id']] = node['id']
    first_node = data_dict['nodes'][0]['id']
    workflows[data_dict["workflow_id"]] = nodes[first_node]
    for edge in data_dict['edges']:
        first_id = outputs[edge['start']]
        second_id = inputs[edge['end']]
        first = nodes[first_id]
        second = nodes[second_id]
        if isinstance(first, TimeNode):
            print(0)
            add_times(first, second)
        first.next_nodes.append(second)
    log("created workflow")


def threaded(c):
    global workflows
    while True:
        data = c.recv(100000)
        if not data:
            print('Bye')
            break
        data_dict = json.loads(data)
        if data_dict['sender'] == 'simulator':
            register_user(data_dict, c)
            break
        else:
            new_workflow(data_dict)
            break


def send_feedback(user_socket, text):
    user_socket.send(text.encode('ascii'))


def Main():
    open('Logger.txt', 'w').close()
    user_lists.init()
    Data.init()
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
