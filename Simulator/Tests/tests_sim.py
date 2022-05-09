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

app = None
lock = threading.Lock()


def handle_questionnaire(questions, user_answers):
    answers = []
    for q in questions:
        answers.append({"question": q, "answer": user_answers[q['text']]})
    return answers


async def get_data(s):
    return await s.recv()


async def actor_simulation(user, s, answers):
    print("hole")
    output = []
    try:
        while True:
            try:
                data = await get_data(s)
            except Exception as e:
                dumpException(e)
            data_json = json.loads(data)
            output.append(data_json)
            if data_json['type'] == 'questionnaire':
                ans = handle_questionnaire(data_json['questions'], answers)
                await s.send(json.dumps(
                    {'type': 'add answers', 'questionnaire_number': data_json['questionnaire_number'], 'id': user['id'],
                     "answers": ans}))
            elif data_json['type'] == 'test data entry':
                val = answers[data_json['test']['name']]
                await s.send(json.dumps(
                    {'type': 'add results', 'id': user['id'], "test": data_json['test']['name'], 'result': val}))
            elif data_json['type'] == 'terminate':
                print("terminated")
                await s.close()
                break

    except Exception as e:
        dumpException(e)
    return user['name'], output


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


# noinspection PyTypeChecker
async def run(path, ans_path, participant_id, gender, age):
    url = "ws://127.0.0.1:7890"
    await send_json(url, path)
    for user in users:
        s = await websockets.connect(url)
        await register_user(user, s)
        user['s'] = s
    f = open(ans_path)
    answers = json.load(f)
    tasks = []
    outputs = {}
    for user in users:
        t = asyncio.create_task(actor_simulation(user, user['s'], answers[user['name']]))
        tasks.append(t)
    user = {"name": "participant " + str(participant_id), "role": "participant", "workflow": 2111561603920,
            "sex": gender, "age": str(age),
            "id": participant_id}

        # noinspection PyBroadException
    try:
        s = await websockets.connect(url)
        await register_user(user, s)
        user['s'] = s
        u, out = await actor_simulation(user, user['s'], answers[user['name']])
        outputs[u] = out
    except Exception as e:
        dumpException(e)
    for t in tasks:
        u, out = await t
        outputs[u] = out
    return outputs


async def send_json(url, path):
    try:
        f = open(path)
        data = json.load(f)
        data['type'] = "add workflow"
        data['workflow_id'] = 2111561603920
        s = await websockets.connect(url)
        await s.send(json.dumps(data))
    except Exception as e:
        dumpException(e)
