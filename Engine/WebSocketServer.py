# Importing the relevant libraries
import json
from _thread import start_new_thread

import websockets
import asyncio

import Data
import NotificationHandler
import user_lists
from Server import register_user, new_workflow

PORT = 7890


# The main behavior function for this server
async def get_notifications(websocket, path):
    print("A client just connected")
    # Handle incoming messages
    try:
        message= await websocket.recv()
        data_dict = json.loads(message)
        print(data_dict)
        if(data_dict['type']=='register'):
            NotificationHandler.connections[data_dict['id']]=websocket
            asyncio.create_task(register_user(data_dict))
        elif (data_dict['type'] =='add workflow'):
            new_workflow(data_dict)
        elif (data_dict['type'] =='add answers'):
            Data.add_questionnaire(data_dict, data_dict['id'])

    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

def Main():
    open('Logger.txt', 'w').close()
    user_lists.init()
    Data.init()
    NotificationHandler.init()
    # Start the server
    start_server = websockets.serve(get_notifications, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    Main()

