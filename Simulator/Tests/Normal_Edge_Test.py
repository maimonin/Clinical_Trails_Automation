import asyncio
import tests_sim
from Database import Database
from Database.DALEdges import DALFixedTimeEdge, DALNormalEdge


async def test():
    Database.delete_db()
    await tests_sim.run('jsons/normal edge example.json', 'Answers/no_answers.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert isinstance(Database.getEdge(1890421297696), DALNormalEdge), "edge is not normal"
    print("passed")


asyncio.run(test())
