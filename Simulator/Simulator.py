import json
import socket
import sys
import threading
from _thread import start_new_thread

from PyQt5 import QtCore, QtGui, QtWidgets
from nodeeditor.utils import dumpException
from windows.multi_question_gui import Ui_multy_question_gui
from windows.open_question_gui import Ui_open_question_gui
from windows.radio_question_gui import Ui_radio_question_gui
from windows.test_enter_gui import Ui_Test_Dialog

host = '127.0.0.1'
port = 8000

user_id = 0
users = [{"name": "nurse", "role": "nurse", "sex": "male", "age": 30},
         {"name": "investigator", "role": "investigator", "sex": "female", "age": 30},
         {"name": "lab", "role": "lab", "sex": "male", "age": 30},
         {"name": "doctor", "role": "doctor", "sex": "female", "age": 30},
         {"name": "participant1", "role": "participant", "workflow": 0, "sex": "male", "age": 30}]
#  {"name": "participant2", "role": "participant", "workflow": 0, "sex": "female", "age": 30}]

app = None
lock = threading.Lock()


def create_questionnaire(questions, call):
    print("create")
    first = None
    prev = None
    for q in questions:
        if q['type'] == 'open':
            curr = Ui_open_question_gui(q)
        elif q['type'] == 'radio':
            curr = Ui_radio_question_gui(q)
        else:
            curr = Ui_multy_question_gui(q)
        curr.callback = call
        if first is None:
            first = curr
        else:
            prev.next = curr
        prev = curr
    return first


def create_tests(tests, call):
    first = None
    prev = None
    for t in tests:
        curr = Ui_Test_Dialog(t)
        curr.callback = call
        if first is None:
            first = curr
        else:
            prev.next = curr
        prev = curr
    return first


def run_wind(ui):
    global app
    app = QtWidgets.QApplication(sys.argv)
    open_question_gui = QtWidgets.QDialog()
    ui.setupUi(open_question_gui)
    open_question_gui.show()
    sys.exit(app.exec_())


def participant_simulation(user):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        register_user(user, s)
        while True:
            data = s.recv(5000)
            print(data)
            data_json = json.loads(data)
            if data_json['type'] == 'notification':
                print("notification")
            #     tabs[data_json['user']].append(data_json('notification'))
            if data_json['type'] == 'questionnaire':
                ans = []

                def callback(answers):
                    ans.append(answers)

                first = create_questionnaire(data_json['questions'], callback)
                t = threading.Thread(target=run_wind, args=(first,))
                t.start()
                t.join()
                print("gonna send answers")
                s.send(json.dumps({"answers": ans}).encode('ascii'))
            elif data_json['type'] == 'test':
                ans = []

                def callback(answers):
                    ans.append(answers)

                first = create_questionnaire(data_json['tests'], callback)
                question_gui = QtWidgets.QDialog()
                first.setupUi(question_gui)
                question_gui.show()
                s.send(json.dumps({"tests": ans}).encode('ascii'))
        # elif data_json['type'] == 'test':
    except Exception as e:
        dumpException(e)


def staff_simulation(user):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        register_user(user, s)
        while True:
            data = s.recv(5000)
            print(data)
    except Exception as e:
        dumpException(e)


def register_user(user, s):
    global user_id
    user_dict = {'sender': 'simulator', 'type': 'add user', 'id': user_id}
    user_dict.update(user)
    message = json.dumps(user_dict)
    user_id += 1
    s.send(message.encode('ascii'))


def Main():
    threads = []
    for user in users:
        if user['role'] == 'participant':
            threads.append(threading.Thread(target=participant_simulation, args=(user,)))
        else:
            threads.append(threading.Thread(target=staff_simulation, args=(user,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    Main()
