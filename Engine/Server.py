import socket
from _thread import *
import threading
from random import randint

import networkx as nx

print_lock = threading.Lock()

nurses = []
doctors = []
labs = []
participants = {}

workflow = nx.DiGraph()


def add_user(user, role):
    if role == "nurse":
        nurses.append(user)
    elif role == "doctor":
        doctors.append(user)
    elif role == "lab":
        labs.append(user)
    elif role == "participant":
        participants[user.id] = user
    log("user "+user.id+" is added")


def get_role(role):
    if role == "nurse":
        return nurses[randint(0, len(nurses) - 1)]
    if role == "doctor":
        return nurses[randint(0, len(doctors) - 1)]
    if role == "lab":
        return nurses[randint(0, len(labs) - 1)]


def addNode(node, participant_id, roles):
    if not participant_id == -1:
        participant = participants.get(participant_id)
        node.attach(participant)
    for role in roles:
        node.attach(get_role(role))
    log("node " + node.id + " is added")


def request_data(participant, message, actor):



def threaded(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')
            print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

    # connection closed
    c.close()


def log(message):
    f = open("Logger.txt", "w")
    f.write(message + '\n')
    f.close()


def Main():
    host = "localhost"
    port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    log("socket binded to port")

    # put the socket into listening mode
    s.listen(5)
    log("socket is listening")

    while True:
        c, addr = s.accept()
        print_lock.acquire()
        log('Connected to :', addr[0], ':', addr[1])

        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
