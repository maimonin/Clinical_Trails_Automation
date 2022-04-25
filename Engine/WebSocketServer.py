# Importing the relevant libraries
import json
from _thread import start_new_thread
from asyncio import sleep

import websockets
import asyncio

import Data
import NotificationHandler
import Server
import user_lists
from Server import register_user, new_workflow, parser_init

PORT = 7890


# The main behavior function for this server
async def get_notifications(websocket, path):
    print("A client just connected")
    # Handle incoming messages
    try:
        async for message in websocket:
            data_dict = json.loads(message)
            print(data_dict)
            if(data_dict['type']=='register'):
                NotificationHandler.connections[data_dict['id']]=websocket
                await asyncio.create_task(register_user(data_dict))
            elif (data_dict['type'] =='add workflow'):
                Server.workflows[data_dict["workflow_id"]]=new_workflow(data_dict)
            elif (data_dict['type'] =='add answers'):
                Data.add_questionnaire(data_dict, data_dict['id'])
            elif (data_dict['type'] =='add results'):
                Data.add_test(data_dict, data_dict['id'])
    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

def Main():
    open('Logger.txt', 'w').close()
    user_lists.init()
    Data.init()
    parser_init()
    NotificationHandler.init()
    # Start the server
    start_server = websockets.serve(get_notifications, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    Main()
