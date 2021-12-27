import json
import socket
from _thread import *
import threading

from Data import get_test_result
from Engine.Nodes import Questionnaire, TestNode, Decision, StringNode
from Logger import log
from Users import add_user

workflows = {}
print_lock = threading.Lock()
OP_NODE_QUESTIONNAIRE = 1
OP_NODE_DATA_ENTRY = 2
OP_NODE_DECISION = 3
OP_NODE_STRING = 4


def parse_Questionnaire(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = Questionnaire(node_dict['id'], node_details['title'], content['questions'])
    return node


def parse_Test(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = TestNode(node_dict['id'], node_details['title'], content['tests'], node_details['actor in charge'])
    return node


def parse_trait_condition(satisfy, trait):
    if satisfy['type'] == 'range':
        values = satisfy['value']
        return lambda patient: True if values['min'] <= patient.get_traits()[trait] <= values['max'] else False
    else:
        return lambda patient: True if trait == satisfy['value'] else False


# def parse_questionnaire_condition(satisfy, trait):
#     if satisfy['type'] == 'range':
#         values = satisfy['value']
#         return lambda patient: True if values['min'] <= trait <= values['max'] else False
#     else:
#         return lambda patient: True if trait == satisfy['value'] else False


def parse_test_condition(satisfy, test_name):
    if satisfy['type'] == 'range':
        values = satisfy['value']
        return lambda patient: True if values['min'] <= get_test_result(patient, test_name) <= values['max'] else False
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
        # elif condition['questionnaire condition']:
        #     combined_condition.append(parse_questionnaire_condition(condition['satisfy'], condition['test']))
        elif condition['type'].rstrip() == 'test condition':
            combined_condition.append(parse_test_condition(condition['satisfy'], condition['test']))
    node = Decision(node_dict['id'], node_details['title'], node_details['actor in charge'], combined_condition)
    return node


def parse_String_Node(node_dict):
    node = StringNode(node_dict['id'], node_dict['title'], node_dict['content'])
    return node


def register_user(user_dict, c):
    user = add_user(user_dict['role'], user_dict['sex'], user_dict['age'], user_dict['id'], c)
    log("user " + user.role + " received")
    if user.role == "participant":
        if len(workflows) == 0:
            print("No workflow yet")
            c.close()
        else:
            # start participant's workflow
            workflows[user_dict["workflow"]].attach(user)
            workflows[user_dict["workflow"]].exec()


def new_workflow(data_dict, c):
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
        # label= edge['label']
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
        else:
            new_workflow(data_dict, c)
            break

    c.close()


def send_feedback(user_socket, text):
    user_socket.send(text.encode('ascii'))


def Main():
    open('Logger.txt', 'w').close()
    host = ""
    port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    log("socket bound to port")

    # put the socket into listening mode
    s.listen(5)
    log("socket is listening")

    while True:
        c, addr = s.accept()
        log('Connected to client')
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
