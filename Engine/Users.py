import json
import time
from Logger import log


def get_data(s):
    data = ""
    curr = s.recv(1)
    curr=curr.decode()
    while curr != "$":
        data += curr
        curr = s.recv(1)
        curr = curr.decode()
    return data


class User:
    def __init__(self, role, sex, age, user_id):
        self.role = role
        self.sex = sex
        self.age = age
        self.id = user_id

    def update(self, callback) -> None:
        callback()

    def get_traits(self):
        return {"gender": self.sex, "age": self.age}

    def to_json(self):
        return {'role':self.role, 'age': self.age, 'id':self.id, 'sex': self.sex}






