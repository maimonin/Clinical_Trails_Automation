import asyncio
import tests_sim
from Database import Database
from Database.DALEdges import DALFixedTimeEdge


async def test():
    Database.delete_db()
    await tests_sim.run('jsons/merge_example.json', 'Answers/no_answers.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert all(x in Database.getStringNodes() for x in
               [(1530916980720, "hello"), (1530916980672, "world"), (1530917076416, "world2"),
                (1530917076944, "done")]), "not all string nodes saved"
    assert all(x in Database.getActorsToNofity() for x in
               [(1530916980720, "Participant"), (1530916980672, "Participant"), (1530917076416, "Participant"),
                (1530917076944, "Participant")]), "not all actors to notify saved"
    print("passed")


asyncio.run(test())
