import asyncio
import tests_sim
from Database import Database


async def test_test():
    Database.delete_db()
    out = await tests_sim.run('jsons/test example.json', 'Answers/test_test_answers1.json',
                              1, 'female', 20)
    assert out == ['{"type": "notification", "text": "show up to hemoglobin"}', '{"type": "notification", "text": '
                                                                                '"show up to A1C test"}',
                   '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_test passed")


asyncio.run(test_test())
