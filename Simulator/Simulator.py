import json
import socket
from _thread import start_new_thread

from PyQt5 import QtCore, QtGui, QtWidgets
from nodeeditor.utils import dumpException
from windows.multi_question_gui import Ui_multy_question_gui
from windows.open_question_gui import Ui_open_question_gui
from windows.radio_question_gui import Ui_radio_question_gui

host = '127.0.0.1'
port = 8000

user_id = 0
users = [{"name": "nurse", "role": "nurse"},
         {"name": "investigator", "role": "investigator"},
         {"name": "lab", "role": "lab"},
         {"name": "doctor", "role": "doctor"},
         {"name": "participant1", "role": "participant", "workflow": 0},
         {"name": "participant2", "role": "participant", "workflow": 0}]


def create_questionnaire(self, questions):
    first = None
    prev = None
    for q in questions:
        if q['type'] == 'open':
            curr = Ui_open_question_gui(q)
        elif q['type'] == 'radio':
            curr = Ui_radio_question_gui(q)
        else:
            curr = Ui_multy_question_gui(q)
        if first is None:
            first = curr
        else:
            prev.next = curr
        prev = curr
    return first


def participant_simulation(self, user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    register_user(user, s)
    data = s.recv(5000)
    data_json = json.loads(data)
    # if data_json['type'] == 'notification':
    #     tabs[data_json['user']].append(data_json('notification'))
    if data_json['type'] == 'questionnaire':
        first = create_questionnaire(data_json['questions'])
        ans=[]
        question_gui = QtWidgets.QDialog()
        first.setupUi(question_gui)
        def callback(answers):
            ans.append(answers)
        first.callback=callback
        question_gui.show()
        s.send(json.dumps(ans))



# elif data_json['type'] == 'test':
#     do_test(data_json['user'], data_json['questions'], s)

def register_user(self, user, s):
    global user_id
    message = json.dumps({'sender': 'simulator', 'type': 'add user', 'role': user["role"], 'id': user_id})
    user_id += 1
    s.send(message.encode('ascii'))


def Main():
    for user in users:
        if user['role'] == 'participant':
            start_new_thread(participant_simulation, (user,))
    while True:
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break


if __name__ == '__main__':
    Main()
