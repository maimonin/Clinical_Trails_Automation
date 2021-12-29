import json
import socket
import threading
from nodeeditor.utils import dumpException

host = '127.0.0.1'
port = 8000

user_id = 0
users = [{"name": "nurse", "role": "nurse", "sex": "male", "age": 30},
         {"name": "nurse2", "role": "nurse", "sex": "male", "age": 30},
         {"name": "investigator", "role": "investigator", "sex": "female", "age": 30},
         {"name": "lab", "role": "lab", "sex": "male", "age": 30},
         {"name": "doctor", "role": "doctor", "sex": "female", "age": 30},
         {"name": "participant1", "role": "participant", "workflow": 0, "sex": "male", "age": 30},
         {"name": "participant2", "role": "participant", "workflow": 0, "sex": "female", "age": 30}]

app = None
lock = threading.Lock()


def handle_open_question(q):
    return {"question": q, "answer": input(q['text'])}


def handle_radio_question(q):
    print(q['text'])
    i = 0
    for opt in q['options']:
        print(str(i) + ". " + opt)
        i += 1
    val = input("type answer number:")
    val = int(val)
    ans=[]
    ans.append(val+1)
    return {"question": q, "answer":ans}


def handle_multi_question(q):
    ans = []
    print(q['text'])
    i = 0
    for opt in q['options']:
        print(str(i) + ". " + opt)
        i += 1
    val = input("type answer number:")
    val=int(val)
    ans.append(val+1)
    while val != -1:
        val = input("type answer number or -1 to finish:")
        val = int(val)
        if val != -1:
            ans.append(val+1)
    return {"question": q, "answer": ans}


def handle_questionnaire(questions, participant):
    lock.acquire()
    answers = []
    print(participant["name"] + " please answer questionnaire:")
    for q in questions:
        if q['type'] == 'open':
            answers.append(handle_open_question(q))
        elif q['type'] == 'radio':
            answers.append(handle_radio_question(q))
        else:
            answers.append(handle_multi_question(q))
    lock.release()
    return answers


def actor_simulation(user, s):
    try:
        while True:
            data = s.recv(5000)
            data_json = json.loads(data)
            if data_json['type'] == 'notification':
                lock.acquire()
                print(user["name"] + " got notification: " + data_json['text'])
                lock.release()
            if data_json['type'] == 'questionnaire':
                ans = handle_questionnaire(data_json['questions'], user)
                s.send(json.dumps({"answers": ans}).encode('ascii'))
            elif data_json['type'] == 'test':
                lock.acquire()
                print(
                    f"{user['name']}:  patient with id {data_json['patient']} is about to arrive please take test:"
                    f" {data_json['name']}  \nthe instructions for this test are: {data_json['instructions']}")
                lock.release()
            elif data_json['type'] == 'test data entry':
                lock.acquire()
                val = input(
                    f"{user['name']}:  patient with id {data_json['patient']} has taken test: "
                    f"{data_json['test']['name']}  \nplease enter the results:")
                lock.release()
                s.send(json.dumps({"test": data_json['test']['name'], 'result': val}).encode('ascii'))
            elif data_json['type'] == 'terminate':
                s.close()
                break

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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        register_user(user, s)
        user['s'] = s
    for user in users:
        threads.append(threading.Thread(target=actor_simulation, args=(user, user['s'])))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    Main()
