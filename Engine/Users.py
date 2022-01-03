import json
import time
from random import randint

from Logger import log
import user_lists


class User:
    def __init__(self, role, sex, age, user_id, socket):
        self.role = role
        self.sex = sex
        self.age = age
        self.id = user_id
        self.socket = socket

    def update(self, callback) -> None:
        callback()

    def get_traits(self):
        return {"gender": self.sex, "age": self.age}


def add_user(role, sex, age, user_id, socket):
    user = User(role, sex, age, user_id, socket)
    if role == "nurse":
        user_lists.nurses.append(user)
    elif role == "doctor":
        user_lists.doctors.append(user)
    elif role == "investigator":
        user_lists.investigators.append(user)
    elif role == "lab":
        user_lists.labs.append(user)
    elif role == "participant":
        user_lists.participants[user.id] = user

    return user


def get_role(role):
    if str(role).lower() == "nurse":
        if len(user_lists.nurses) == 0:
            print("no available nurse")
            return None
        return user_lists.nurses[randint(0, len(user_lists.nurses) - 1)]
    if str(role).lower() == "doctor":
        if len(user_lists.doctors) == 0:
            print("no available doctor")
            return None
        return user_lists.doctors[randint(0, len(user_lists.doctors) - 1)]
    if str(role).lower() == "investigator":
        if len(user_lists.investigators) == 0:
            print("no available investigator")
            return None
        return user_lists.investigators[randint(0, len(user_lists.investigators) - 1)]
    if str(role).lower() == "lab":
        if len(user_lists.labs) == 0:
            print("no available lab worker")
            return None
        return user_lists.labs[randint(0, len(user_lists.labs) - 1)]


def answer_questionnaire(questions, s):
    s.send(json.dumps({'type': 'questionnaire', 'questions': questions}).encode('ascii'))
    ans = s.recv(5000)
    log("answering questionnaire")
    return json.loads(ans)


# name, instructions, staff
def take_test(user_id, test, in_charge, s):
    for role in test.staff:
        get_role(role).socket.send(json.dumps({'type': 'test', 'name': test.name,
                                               'instructions': test.instructions,
                                               'patient': user_id}).encode('ascii'))
    s.send(json.dumps({'type': 'notification', 'text': "show up to " + test.name}).encode('ascii'))
    log("participant with id " + str(user_id) + " taking a test")
    time.sleep(int(test.duration))
    form = {'type': 'test data entry', 'test': test.to_json(), 'patient': user_id}
    r = get_role(in_charge)
    r.socket.send(json.dumps(form).encode('ascii'))
    results = r.socket.recv(5000)
    return json.loads(results)
