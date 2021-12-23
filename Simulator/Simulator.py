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
            message = json.dumps({'sender': 'simulator', 'role': user["role"], 'id': user_id})
            user_id += 1
            s.send(message.encode('ascii'))
            data = s.recv(1024)
            data_json = json.loads(data)
            if data_json['type'] == 'connect':
                tabs[int(data_json['id'])] = []
                print("tab for "+str(data_json['id'])+" opened")

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    s.close()


if __name__ == '__main__':
    Main()
