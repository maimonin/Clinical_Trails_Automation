import json
from random import randint

from Logger import log

nurses = []
doctors = []
investigators = []
labs = []
participants = {}


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
        return {"sex": self.sex, "age": self.age}


def add_user(role, sex, age, user_id, socket):
    print(len(nurses))
    user = User(role, sex, age, user_id, socket)
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
    log("user " + str(user.id) + " is added")
    return user


def get_role(role):
    if role == "nurse":
        return nurses[0]
#        return nurses[randint(0, len(nurses) - 1)]
    if role == "doctor":
        return doctors[0]
#        return nurses[randint(0, len(doctors) - 1)]
    if role == "investigator":
        return investigators[0]
#        return investigators[randint(0, len(investigators) - 1)]
    if role == "lab":
        return labs[0]
#        return nurses[randint(0, len(labs) - 1)]


def answer_questionnaire(questions, s):
    print("1")
    s.send(json.dumps({'type': 'questionnaire', 'questions': questions}).encode('ascii'))
    print("2")
    ans = s.recv(5000)
    print("3")
    log("answering questionnaire")
    print("4")
    return json.loads(ans)


# name, instructions, staff
def take_test(user_id, test, in_charge, s):
    for role in test['staff']:
        get_role(role).socket.send(json.dumps({'type': 'test', 'name': test['name'],
                                               'instructions': test['instructions'],
                                               'patient': user_id}))
    s.send(json.dumps({'type': 'notification', 'text': "show up to "+test['name']}))
    form = {'type': 'test data entry','test': test, 'patient': user_id}
    get_role(in_charge).socket.send(json.dumps(form).encode('ascii'))
    results = get_role(in_charge).socket(5000)
    log("taking a test")
    return json.loads(results)


