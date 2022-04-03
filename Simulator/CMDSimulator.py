import asyncio
import json
import threading
import websockets
from nodeeditor.utils import dumpException

user_id = 0
users = [{"name": "nurse", "role": "nurse", "sex": "male", "age": 30},
         {"name": "investigator", "role": "investigator", "sex": "female", "age": 30},
         {"name": "lab", "role": "lab technician", "sex": "male", "age": 30},
         {"name": "doctor", "role": "doctor", "sex": "female", "age": 30}]
# {"name": "participant1", "role": "participant", "workflow": 0, "sex": "male", "age": 30},
# {"name": "participant2", "role": "participant", "workflow": 0, "sex": "female", "age": 30}]

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
    ans = []
    ans.append(val + 1)
    return {"question": q, "answer": ans}


def handle_multi_question(q):
    ans = []
    print(q['text'])
    i = 0
    for opt in q['options']:
        print(str(i) + ". " + opt)
        i += 1
    val = input("type answer number:")
    val = int(val)
    ans.append(val + 1)
    while val != -1:
        val = input("type answer number or -1 to finish:")
        val = int(val)
        if val != -1:
            ans.append(val + 1)
    return {"question": q, "answer": ans}


def handle_questionnaire(questions, participant):
    lock.acquire()
    answers = []
    print(participant["name"] + " please answer questionnaire:")
    for q in questions:
        if q['type'] == 'open':
            answers.append(handle_open_question(q))
        elif q['type'] == 'one choice':
            answers.append(handle_radio_question(q))
        else:
            answers.append(handle_multi_question(q))
    lock.release()
    return answers


async def get_data(s):
    return await s.recv()


async def actor_simulation(user, s):
    try:
        while True:
            try:
                data = await get_data(s)
            except:
                break
            print(data)
            data_json = json.loads(data)
            if data_json['type'] == 'notification':
                lock.acquire()
                print(user["name"] + " got notification: " + data_json['text'])
                lock.release()
            if data_json['type'] == 'questionnaire':
                ans = handle_questionnaire(data_json['questions'], user)
                await s.send(json.dumps(
                    {'type': 'add answers', 'questionnaire_number': data_json['questionnaire_number'], 'id': user['id'],
                     "answers": ans}))
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
                await s.send(json.dumps(
                    {'type': 'add results', 'id': user['id'], "test": data_json['test']['name'], 'result': val}))
            elif data_json['type'] == 'terminate':
                await s.close()
                break

    except Exception as e:
        dumpException(e)


async def register_user(user, s):
    global user_id
    user_dict = {'type': 'register', 'id': user_id}
    user_dict.update(user)
    message = json.dumps(user_dict)
    user_id += 1
    await s.send(message)


async def login_user(log_id, s):
    await s.send(json.dumps({'type': 'sign in', 'id': log_id}))
    return await get_data(s)


async def Main():
    threads = []
    url = "ws://127.0.0.1:7890"
    #await send_json(url)
    for user in users:
        s = await websockets.connect(url)
        await register_user(user, s)
        user['s'] = s
    for user in users:
        asyncio.create_task(actor_simulation(user, user['s']))
    while True:
        lock.acquire()
        inp = input('to register user press r, to log in user press l')
        lock.release()
        # url = "ws://127.0.0.1:7890"
        if inp == 'r':
            lock.acquire()
            id = int(input('id'))
            gender = input('gender')
            age = int(input('age'))
            lock.release()
            user = {"name": "participant " + str(id), "role": "participant", "workflow": 2111561603920,
                    "sex": gender, "age": age,
                    "id": id}
            is_cn = True
            while is_cn:
                try:
                    s = await websockets.connect(url)
                    await register_user(user, s)
                    user['s'] = s
                    asyncio.create_task(actor_simulation(user, user['s']))
                    is_cn = False
                except:
                    continue
            lock.acquire()
            print('registered')
            lock.release()
        elif inp == 'l':
            lock.acquire()
            log_id = int(input('id'))
            lock.release()
            is_cn = True
            while is_cn:
                try:
                    s = await websockets.connect(url)
                    user = await login_user(log_id, s)
                    asyncio.create_task(actor_simulation(user, user['s']))
                    is_cn = False
                except:
                    continue

        await asyncio.sleep(10)


async def send_json(url):
    path = input("workflow path:")
    try:
        f = open(path)
        data = json.load(f)
        print(data)
        data['type'] = "add workflow"
        data['workflow_id'] = 2111561603920
        s = await websockets.connect(url)
        await s.send(json.dumps(data))
    except Exception as e:
        dumpException(e)


asyncio.run(Main())
