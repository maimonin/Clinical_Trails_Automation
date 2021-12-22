import json
import socket
from _thread import *
import threading
from random import randint

from Engine.Nodes import DataEntering
from Engine.User import User

nurses = []
doctors = []
investigators = []
labs = []
participants = {}

workflow = None
print_lock = threading.Lock()


def add_user(user, role):
    if role == "nurse":
        nurses.append(user)
    elif role == "doctor":
        doctors.append(user)
    elif role == "investigator":
        investigators.append(user)
    elif role == "lab":
        labs.append(user)
    elif role == "participant":
        participants[user.id] = user
    log("user " + user.id + " is added")


def get_role(role):
    if role == "nurse":
        return nurses[randint(0, len(nurses) - 1)]
    if role == "doctor":
        return nurses[randint(0, len(doctors) - 1)]
    if role == "lab":
        return nurses[randint(0, len(labs) - 1)]


def addNode(json, roles):
    id = 0
    log("node " + id + " is added")


def request_data(participant, message, actor):
    return None


def parse_Questionnaire(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = DataEntering(node_dict['id'], node_details['title'], node_details['actor in charge'], content['questions'])
    return node

def parse_Test(node_dict):
    content = node_dict['content']
    node_details = content['node_details']
    node = DataEntering(node_dict['id'], node_details['title'], node_details['actor in charge'], content['tests'])
    return node


def threaded(c):
    global workflow
    while True:
        data = c.recv(5000)
        if not data:
            print('Bye')
            print_lock.release()
            break

        data_dict = json.loads(data)
        if data_dict['sender'] == 'simulator':
            user_dict = data_dict
            user = User(user_dict['role'], user_dict['id'], c)
            log("user " + user_dict['role'] + " received")
            c.send(str(user_dict['id']).encode('ascii'))
            if user.role == "participant":
                participants['id'] = user
                workflow.attach(user)
                workflow.exec()
        else:
            nodes = {}
            outputs={}
            inputs={}
            print(data_dict)
            for node in data_dict['nodes']:
                if node['title'] == 'Questionnaire':
                    nodes[node['id']] = parse_Questionnaire(node)
                elif node['title'] == 'Data Entry':
                    nodes[node['id']] = parse_Test(node)
                if node['title'] != 'Decision':
                    for out in node['outputs']:
                        outputs[out['id']]=node['id']
                    for inp in node['inputs']:
                        inputs[inp['id']] = node['id']
            first_node=data_dict['nodes'][0]['id']
            workflow=nodes[first_node]
            for edge in data_dict['edges']:
                first_id=outputs[edge['start']]
                second_id = inputs[edge['end']]
                first= nodes[first_id]
                second = nodes[second_id]
                # label= edge['label']
                first.next = second

            break

    c.close()


def send_feedback(user_socket, text):
    user_socket.send(text.encode('ascii'))


def log(message):
    f = open("Logger.txt", "a")
    f.write(message + '\n')
    f.close()


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
        print_lock.acquire()
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
