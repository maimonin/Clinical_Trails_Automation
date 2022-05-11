# Importing the relevant libraries
import json
import websockets
import asyncio
import Data
import NotificationHandler
import Parser
import user_lists
from Database import Database
from Parser import register_user, new_workflow, parser_init

PORT = 7890


# The main behavior function for this server
async def get_notifications(websocket, path):
    print("A client just connected")
    # Handle incoming messages
    try:
        async for message in websocket:
            data_dict = json.loads(message)
            if data_dict['type'] == 'register':
                NotificationHandler.connections[data_dict['id']] = websocket
                asyncio.create_task(register_user(data_dict))
            elif data_dict['type'] == 'sign in':
                NotificationHandler.connections[data_dict['id']] = websocket
                # Parser.load_workflow(data_dict['id'])
                user = Database.getUser(data_dict['id'])
                await websocket.send(json.dumps(user.to_json()))
            elif data_dict['type'] == 'add workflow':
                new_workflow(data_dict)
            elif data_dict['type'] == 'load workflow':
                Parser.load_workflow(data_dict["workflow_id"])
            elif data_dict['type'] == 'add answers':
                Data.add_questionnaire(data_dict, data_dict['id'])
            elif data_dict['type'] == 'add results':
                Data.add_test(data_dict['test'], data_dict, data_dict['id'])
            elif data_dict['type'] == 'change db':
                Database.set_name('Database/test_data.db')
                Database.init_tables()
    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")


def Main():
    open('Logger.txt', 'w').close()
    user_lists.init()
    Data.init()
    parser_init()
    Database.init_tables()
    NotificationHandler.init()
    # Start the server
    start_server = websockets.serve(get_notifications, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    Main()
