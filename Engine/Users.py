import json
import time
import Scheduler
from Logger import log
from user_lists import get_role


def get_data(s):
    data = ""
    curr = s.recv(1)
    while curr != "$":
        data += curr
        curr = s.recv(1)
    return data


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


def answer_questionnaire(questions, s):
    s.send((json.dumps({'type': 'questionnaire', 'questions': questions}) + '$').encode('ascii'))
    ans = get_data(s)
    log("answering questionnaire")
    return json.loads(ans)


# name, instructions, staff
def take_test(user_id, test, remaining_time, in_charge, s):
    for role in test.staff:
        actor = Scheduler.get_role(role, remaining_time)
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
