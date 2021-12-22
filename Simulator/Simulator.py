import json
import socket

user_id = 0
roles = ["nurse", "doctor", "investigator", "lab", "participant"]
tabs = {}


def Main():
    host = '127.0.0.1'
    port = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        global user_id
        for role in roles:
            message = json.dumps({'sender': 'simulator', 'role': role, 'id': user_id})
            user_id += 1
            s.send(message.encode('ascii'))
            data = int(s.recv(1024))
            tabs[data] = []
            print("tab for "+str(data)+" opened")
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    s.close()


if __name__ == '__main__':
    Main()
