import json
import time
from random import randint

from Logger import log
from Users import User


def init():
    global nurses
    global doctors
    global investigators
    global labs
    global participants
    nurses = []
    doctors = []
    investigators = []
    labs = []
    participants = {}


def get_role(role):
    if str(role).lower() == "nurse":
        if len(nurses) == 0:
            print("no available nurse")
            return None
        return nurses[randint(0, len(nurses) - 1)]
    if str(role).lower() == "doctor":
        if len(doctors) == 0:
            print("no available doctor")
            return None
        return doctors[randint(0, len(doctors) - 1)]
    if str(role).lower() == "investigator":
        if len(investigators) == 0:
            print("no available investigator")
            return None
        return investigators[randint(0, len(investigators) - 1)]
    if str(role).lower() == "lab":
        if len(labs) == 0:
            print("no available lab worker")
            return None
        return labs[randint(0, len(labs) - 1)]
    return None


def add_user(role, sex, age, user_id, socket):
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
    return user

# name, instructions, staff
def take_test(user_id, test, in_charge, s):
    for role in test.staff:
        actor = get_role(role)
        if actor is None:
            return None
        actor.socket.send((json.dumps({'type': 'test', 'name': test.name,
                                       'instructions': test.instructions,
                                       'patient': user_id}) + '$').encode('ascii'))
    s.send((json.dumps({'type': 'notification', 'text': "show up to " + test.name})+'$').encode('ascii'))
    log("participant with id " + str(user_id) + " taking a test")
    time.sleep(int(test.duration))
    form = {'type': 'test data entry', 'test': test.to_json(), 'patient': user_id}
    r = get_role(in_charge)
    r.socket.send((json.dumps(form)+'$').encode('ascii'))
    results = get_data(s)
    return json.loads(results)