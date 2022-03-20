import asyncio
import json

from Logger import log


def init():
    global connections
    connections = {}


def send_notification_by_id(id, message):
    loop=None
    try:
        loop=asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if connections[id] is not None:
        print('sending')
        asyncio.get_event_loop().run_until_complete(connections[id].send(json.dumps(message)))
        print('sent')



def send_questionnaire(questions, id, number):
    send_notification_by_id(id, {'type': 'questionnaire', 'number':number,'questions': questions})
    log("sending questionnaire")
