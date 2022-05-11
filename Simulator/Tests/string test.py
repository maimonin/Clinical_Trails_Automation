import asyncio
import tests_sim
from Database import Database


async def test_string():
    Database.delete_db()
    out = await tests_sim.run('jsons/string example.json', 'Answers/no_answers.json',
                              1, 'female', 20)
    assert out == ['{"type": "notification", "text": "hello world"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_string passed")


asyncio.run(test_string())
