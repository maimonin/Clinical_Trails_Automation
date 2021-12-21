import json
import socket
from _thread import *
import threading
from random import randint

from Engine.User import User

nurses = []
doctors = []
labs = []
participants = {}

workflow = None


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


def addNode(json, roles):
    id = 0
    log("node " + id + " is added")


def request_data(participant, message, actor):
    return None


# {'role': 'nurse', 'id': 0}

def threaded(c):
    data = c.recv(1024)
    if not data:
        print('Bye')

    user_dict = json.loads(data)
    user = User(user_dict['role'], user_dict['id'], c)
    log("user received")
    if user.role == "participant":
        participants['id'] = user
        workflow.attach(user)
        workflow.exec()
    c.close()


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
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
