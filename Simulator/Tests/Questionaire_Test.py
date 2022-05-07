import asyncio
import tests_sim
from Database import Database


async def test():
    Database.delete_db(r"C:\Users\Owner\Desktop\Clinical_Trails_Automation\Engine\Database\test_data.db")
    await tests_sim.run('jsons/questionnaire_example.json', 'Answers/questionnaire_example_answers1.json',
                        1, 'female', 20)
    print(Database.getUser(1))
    assert Database.getUser(1).role == "participant", "user sghoulf be participant"
    assert Database.getUser(1).sex == "female", "user should be fdemale"
    assert Database.getUser(1).age == 20, "usere shoudl be 20"
    print("passed")


asyncio.run(test())
