import json
import socket

user_id = 0
users = [{"name": "nurse", "role": "nurse"},
         {"name": "investigator", "role": "investigator"},
         {"name": "lab", "role": "lab"},
         {"name": "doctor", "role": "doctor"},
         {"name": "participant1", "role": "participant", "workflow": 0},
         {"name": "participant2", "role": "participant", "workflow": 0}]
tabs = {}


def Main():
    host = '127.0.0.1'
    port = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        global user_id
        for user in users:
            message = json.dumps({'sender': 'simulator', 'type': 'add user', 'role': user["role"], 'id': user_id})
            user_id += 1
            s.send(message.encode('ascii'))
            data = s.recv(1024)
            data_json = json.loads(data)
            if data_json['type'] == 'connect':
                tabs[int(data_json['id'])] = []
                print("tab for " + str(data_json['id']) + " opened")
            elif data_json['type'] == 'notification':
                tabs[data_json['user']].append(data_json('notification'))
            elif data_json['type'] == 'questions':
                tabs[data_json['user']].append("fill out form")
                for question in data_json['questions']:
                    print(question)
                    if question['type'] == 'multi':
                        print(question['options'])
                    ans = input('\n')
                    s.send(json.dumps(
                        {'sender': 'simulator', 'type': 'answer', 'id': data_json['user'],
                         'answer': ans}).encode('ascii'))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    s.close()


if __name__ == '__main__':
    Main()
