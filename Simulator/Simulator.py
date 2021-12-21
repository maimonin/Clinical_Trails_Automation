# Import socket module
import json
import socket

user_id = 0


def Main():
    host = '127.0.0.1'
    port = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    message = json.dumps({'role': 'nurse', 'id': 0})

    while True:
        s.send(message.encode('ascii'))
        data = s.recv(1024)

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    s.close()


if __name__ == '__main__':
    Main()