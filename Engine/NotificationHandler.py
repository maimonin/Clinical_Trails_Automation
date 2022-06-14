import json
from datetime import datetime

from Logger import log


def init():
    # noinspection PyGlobalUndefined
    global connections
    connections = {}


async def send_notification_by_id(user_id, message):
    if connections[user_id] is not None:
        await connections[user_id].send(json.dumps(message))


async def send_questionnaire(questions, number, user_id):
    await send_notification_by_id(user_id, {'type': 'questionnaire', 'questionnaire_number': number,
                                            'questions': questions})
    log(datetime.now().strftime("%H:%M:%S") + " sending questionnaire")
