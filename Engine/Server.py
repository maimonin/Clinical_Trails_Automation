import json
import socket
from _thread import *
import threading
from Engine.Nodes import DataEntering
from Logger import log
from Users import add_user

workflows = {}
print_lock = threading.Lock()


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
    global workflows
    while True:
        data = c.recv(5000)
        if not data:
            print('Bye')
            print_lock.release()
            break

        data_dict = json.loads(data)
        if data_dict['sender'] == 'simulator':
            user_dict = data_dict
            add_user(user_dict['role'], user_dict['id'], c)
            log("user " + user_dict['role'] + " received")
            connected = json.dumps({'type': 'connect', 'id': user_dict['id']})
            c.send(connected.encode('ascii'))
            if user_dict['role'] == "participant":
                if len(workflows) == 0:
                    print("No workflow yet")
                    c.close()
                else:
                    # start participant's workflow
                    add_user(user_dict['role'], user_dict['id'], c)
                    workflows[user_dict["workflow"]].attach(user_dict['id'])
                    workflows[user_dict["workflow"]].exec()
        else:
            nodes = {}
            outputs = {}
            inputs = {}
            print(data_dict)
            for node in data_dict['nodes']:
                if node['title'] == 'Questionnaire':
                    nodes[node['id']] = parse_Questionnaire(node)
                elif node['title'] == 'Data Entry':
                    nodes[node['id']] = parse_Test(node)
                if node['title'] != 'Decision':
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
                first.next = second

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
        print_lock.acquire()
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
