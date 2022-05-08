import asyncio
import tests_sim
from Database import Database


async def test_age_in_range():
    Database.delete_db()
    out = await tests_sim.run('jsons/trait age condition example.json', 'Answers/trait_gender_answers1.json',
                              1, 'female', 20)
    assert out == ['{"type": "notification", "text": "in range"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_gender_in_range passed")


async def test_age_not_in_range():
    Database.delete_db()
    out = await tests_sim.run('jsons/trait age condition example.json', 'Answers/trait_gender_answers1.json',
                              1, 'female', 45)
    assert out == ['{"type": "notification", "text": "out of range"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 45, "user should be 45"
    print("test_gender_in_range passed")


asyncio.run(test_age_in_range())
asyncio.run(test_age_not_in_range())
