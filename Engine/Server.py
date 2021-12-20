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
    id=0
    log("node " + id + " is added")


def request_data(participant, message, actor):
    return None


# user json
#role
#id

def threaded(c):
    data = c.recv(1024)
    if not data:
        print('Bye')

    user_data = json.loads(data)
    json_obj = json.dumps(user_data)
    useri = User(json_obj['role'],json_obj['id'], c)
    if useri.role=="participant":
        participants['id']=useri
        workflow.attach(useri)
        workflow.exec()
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
        log('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
