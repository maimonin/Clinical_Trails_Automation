import json
from random import randint

from Logger import log

nurses = []
doctors = []
investigators = []
labs = []
participants = {}


class User:
    def __init__(self, role, id, socket):
        self.role = role
        self.id = id
        self.socket = socket

    def update(self, callback) -> None:
        callback()


def add_user(role, user_id, socket):
    user = User(role, user_id, socket)
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
    return user


def get_role(role):
    if role == "nurse":
        return nurses[randint(0, len(nurses) - 1)]
    if role == "doctor":
        return nurses[randint(0, len(doctors) - 1)]
    if role == "lab":
        return nurses[randint(0, len(labs) - 1)]


def answer_questionnaire(user, questions, s):
    s.send(json.dumps({'type': 'questionnaire', 'questions': questions}))
    ans = s.recv(5000)
    return json.loads(ans)