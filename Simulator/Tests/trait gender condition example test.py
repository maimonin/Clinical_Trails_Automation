import asyncio
import tests_sim
from Database import Database


async def test_gender_female():
    Database.delete_db()
    out=await tests_sim.run('jsons/trait gender condition example.json', 'Answers/trait_gender_answers1.json',
                        1, 'female', 20)
    assert out==['{"type": "notification", "text": "you\'re a girl"}', '{"type": "terminate"}']
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("test_gender_female passed")

async def test_gender_male():
    Database.delete_db()
    out=await tests_sim.run('jsons/trait gender condition example.json', 'Answers/trait_gender_answers1.json',
                        2, 'male', 20)
    assert out==['{"type": "notification", "text": "you\'re a boy"}', '{"type": "terminate"}']
    assert Database.getUser(2).role == "participant", "user should be participant"
    assert Database.getUser(2).sex == "male", "user should be male"
    assert Database.getUser(2).age == 20, "user should be 20"
    print("test_gender_male passed")
asyncio.run(test_gender_female())
asyncio.run(test_gender_male())
