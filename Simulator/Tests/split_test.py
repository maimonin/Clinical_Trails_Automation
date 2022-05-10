import asyncio
import tests_sim
from Database import Database


async def test_split():
    Database.delete_db()
    out = await tests_sim.run('jsons/split_example.json', 'Answers/no_answers.json',
                              1, 'female', 20)
    assert (out == ['{"type": "notification", "text": "hello"}','{"type": "notification", "text": "world"}','{"type": "notification", "text": "world2"}', '{"type": "terminate"}']
            or out == ['{"type": "notification", "text": "hello"}','{"type": "notification", "text": "world2"}','{"type": "notification", "text": "world"}', '{"type": "terminate"}'])
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_split passed")


asyncio.run(test_split())
