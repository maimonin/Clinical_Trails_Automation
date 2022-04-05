import json
import time
from asyncio import sleep
from random import randint

from Database import Database
from Logger import log
from NotificationHandler import send_notification_by_id
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
    actor = Database.getStaff(role)
    if actor is None:
        print("no available staff member")
    return actor


def add_user(role, sex, age, user_id):
    user = User(role, sex, age, user_id)
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
async def take_test(user_id, test, in_charge):
    for role in test.staff:
        actor = get_role(role)
        if actor is None:
            return None
        await send_notification_by_id(actor.id, {'type': 'test', 'name': test.name,
                                                 'instructions': test.instructions,
                                                 'patient': user_id})
    await send_notification_by_id(user_id, {'type': 'notification', 'text': "show up to " + test.name})
    log("participant with id " + str(user_id) + " taking a test")
    await sleep(int(test.duration))
    form = {'type': 'test data entry', 'test': test.to_json(), 'patient': user_id}
    # r = get_role(in_charge)
    await send_notification_by_id(user_id, form)
