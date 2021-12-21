# Import socket module
import socket

user_id = 0


def Main():
    host = '127.0.0.1'
    port = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    message = "shaurya says geeksforgeeks"
    while True:
        s.send(message.encode('ascii'))

        # message received from server
        data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :', str(data.decode('ascii')))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    s.close()


if __name__ == '__main__':
    Main()