import asyncio
import tests_sim
from Database import Database


async def test():
    Database.delete_db()
    print('here')
    await tests_sim.run('jsons/questionnaire_example.json', 'Answers/questionnaire_example_answers1.json',
                        1, 'female', 20)
    print(Database.getUser(1).role)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    print("passed")


asyncio.run(test())
