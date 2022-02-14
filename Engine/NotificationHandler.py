import json

from Logger import log


def init():
    global connections
    connections = {}


# @TODO should probebly change for async later
async def send_notification_by_id(id, message):
    if connections[id] is not None:
        await connections[id].send(json.dumps(message))

async def send_questionnaire(questions,id):
    await send_notification_by_id(id,{'type': 'questionnaire', 'questions': questions})
    log("sending questionnaire")