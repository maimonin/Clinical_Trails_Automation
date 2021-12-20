import socket
from _thread import *
import threading

print_lock = threading.Lock()


def threaded(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')
            print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

    # connection closed
    c.close()


def log(message):
    f = open("Logger.txt", "w")
    f.write(message + '\n')
    f.close()


def Main():
    host = "localhost"
    port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    log("socket binded to port")

    # put the socket into listening mode
    s.listen(5)
    log("socket is listening")

    while True:
        c, addr = s.accept()
        print_lock.acquire()
        log('Connected to :', addr[0], ':', addr[1])

        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
