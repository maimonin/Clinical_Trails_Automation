import asyncio
import tests_sim
from Database import Database


async def test():
    Database.delete_db()
    await tests_sim.run('jsons/complex example.json', 'Answers/no_answers.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert 2111561603920 in Database.getWorkflowsIds(), "workflows should contain id 2111561603920"
    assert (2453429801216, "hi") in Database.getStringNodes(), "string node not saved"
    assert (2453429713072, 1892803102753) in Database.getComplexNodes(), "complex node not saved"
    assert all(x in Database.getActorsToNofity() for x in
               [(2453429801216, "Doctor"), (2453429801216, "Nurse")]), "not all actors to notify saved"
    print("passed")


asyncio.run(test())
