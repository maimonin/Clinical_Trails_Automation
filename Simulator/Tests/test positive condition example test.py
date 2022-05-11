import asyncio
import tests_sim
from Database import Database


async def test_condition_positive():
    Database.delete_db()
    out = await tests_sim.run('jsons/test positive condition example.json', 'Answers/test_positive_condition_answers1.json',
                              1, 'female', 20)
    assert out == ['{"type": "notification", "text": "show up to antigen"}',
                   '{"type": "notification", "text": "you have been found positive and will not continue trail"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_condition_positive passed")


async def test_condition_negative():
    Database.delete_db()
    out = await tests_sim.run('jsons/test positive condition example.json', 'Answers/test_nagative_condition_answers1.json',
                              1, 'female', 20)
    assert out == ['{"type": "notification", "text": "show up to antigen"}',
                   '{"type": "notification", "text": "continue trail"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_condition_negative passed")


asyncio.run(test_condition_positive())
asyncio.run(test_condition_negative())
