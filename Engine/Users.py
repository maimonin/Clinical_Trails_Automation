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






