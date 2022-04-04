import json

from Logger import log


def init():
    global connections
    connections = {}


async def send_notification_by_id(id, message):
    if connections[id] is not None:
        await connections[id].send(json.dumps(message))


async def send_questionnaire(questions, number, id):
    await send_notification_by_id(id, {'type': 'questionnaire', 'questionnaire_number': number, 'questions': questions})
    log("sending questionnaire")
