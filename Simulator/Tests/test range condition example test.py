import asyncio
import tests_sim
from Database import Database


async def test_condition_in_range():
    Database.delete_db()
    out = await tests_sim.run('jsons/test range condition example.json', 'Answers/test_range_condition_answers1.json',
                              1, 'female', 20)
    assert out == ['{"type": "notification", "text": "show up to hemoglobin"}',
                   '{"type": "notification", "text": "in range"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_condition_in_range passed")


async def test_condition_not_in_range():
    Database.delete_db()
    out = await tests_sim.run('jsons/test range condition example.json', 'Answers/test_range_condition_answers2.json',
                              1, 'female', 20)
    assert out == ['{"type": "notification", "text": "show up to hemoglobin"}',
                   '{"type": "notification", "text": "out of range"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_condition_in_range passed")


asyncio.run(test_condition_in_range())
asyncio.run(test_condition_not_in_range())
