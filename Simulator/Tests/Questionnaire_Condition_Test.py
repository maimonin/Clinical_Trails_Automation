import asyncio
import tests_sim
from Database import Database


async def test_yes_ok():
    Database.delete_db()
    await tests_sim.run('jsons/questionnaire condition example.json',
                        'Answers/questionnaire_condition_example_answers1.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert 2111561603920 in Database.getWorkflowsIds(), "workflows should contain id 2111561603920"
    assert all(x in Database.getQuestions() for x in
               [(1, 1, "Ok?", "one choice")]), "not all questions saved"
    assert (2225378966112, 1) in Database.getQuestionnaires(), "questionnaire not saved"
    assert all(x in Database.getAnswerOptions() for x in [(1, 1, 0, 'yes'), (1, 1, 1, 'no')]), "not all options saved"
    assert Database.getAnswer(1, 1, 1) == [0], "incorrect answer saved for question 1"
    visited_ids = list(map(lambda x: x[1].id, list(filter(lambda x: x[0] == "node", Database.getCurrentPositions(1)))))
    assert 2225389267984 in visited_ids, "wrong decision made"
    assert 2225389267360 not in visited_ids, "wrong decision made"
    print("passed")


async def test_no_ok():
    Database.delete_db()
    await tests_sim.run('jsons/questionnaire condition example.json',
                        'Answers/questionnaire_condition_example_answers2.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert 2111561603920 in Database.getWorkflowsIds(), "workflows should contain id 2111561603920"
    assert all(x in Database.getQuestions() for x in
               [(1, 1, "Ok?", "one choice")]), "not all questions saved"
    assert (2225378966112, 1) in Database.getQuestionnaires(), "questionnaire not saved"
    assert all(x in Database.getAnswerOptions() for x in [(1, 1, 0, 'yes'), (1, 1, 1, 'no')]), "not all options saved"
    assert Database.getAnswer(1, 1, 1) == [1], "incorrect answer saved for question 1"
    visited_ids = list(map(lambda x: x[1].id, list(filter(lambda x: x[0] == "node", Database.getCurrentPositions(1)))))
    assert 2225389267360 in visited_ids, "wrong decision made"
    assert 2225389267984 not in visited_ids, "wrong decision made"
    print("passed")


asyncio.run(test_yes_ok())
asyncio.run(test_no_ok())
