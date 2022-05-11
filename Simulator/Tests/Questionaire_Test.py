import asyncio
import tests_sim
from Database import Database


async def test():
    Database.delete_db()
    await tests_sim.run('jsons/questionnaire_example.json', 'Answers/questionnaire_example_answers1.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert 2111561603920 in Database.getWorkflowsIds(), "workflows should contain id 2111561603920"
    assert all(x in Database.getQuestions() for x in
               [(1, 1, "aaaaa", "multi"), (1, 2, "bbbbb", "one choice"), (1, 3, "ccccc", "open")]),\
        "not all questions saved"
    assert (2111599926624, 1) in Database.getQuestionnaires(), "questionnaire not saved"
    assert all(x in Database.getAnswerOptions() for x in
               [(1, 1, 0, '1'), (1, 1, 1, '2'), (1, 2, 0, '1'), (1, 2, 1, '2')]), "not all options saved"
    assert Database.getAnswer(1, 1, 1) == [0], "incorrect answer saved for question 1"
    assert Database.getAnswer(1, 2, 1) == [0], "incorrect answer saved for question 1"
    assert Database.getAnswer(1, 3, 1) == "hi", "incorrect answer saved for question 1"
    print("passed")


asyncio.run(test())
