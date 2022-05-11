import asyncio
import tests_sim
from Database import Database


async def test1():
    Database.delete_db()
    await tests_sim.run('jsons/covid example.json', 'Answers/covid_answers1.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert 2111561603920 in Database.getWorkflowsIds(), "workflows should contain id 2111561603920"
    assert all(x in Database.getQuestions() for x in
               [(1, 1, "If you join, you will have injections, blood draws, saliva samples, and nasal swabs of your "
                       "nose.", "one choice"),
                (1, 2, "-The most common risks are symptoms are fever, muscle aches and headaches after getting the "
                       "study vaccine. \n-There are other, less serious risks. We will tell you more about them later "
                       "in this consent form. ", "one choice"),
                (1, 3, "Full Name", "open"),
                (2, 1, "Choose your symptoms", "multi"),
                (2, 2, "Any side effect not mentioned you experienced?", "open")
                ]), "not all questions saved"
    assert all(x in Database.getQuestionnaires() for x in [(2846458731440, 1), (2846460297376, 2)]),\
        "questionnaire not saved"
    assert all(x in Database.getAnswerOptions() for x in [(1, 1, 0, 'Agree'), (1, 1, 1, 'No'), (1, 2, 0, 'Agree'),
                                                          (1, 2, 1, 'No'), (2, 1, 0, 'Fever'),
                                                          (2, 1, 1, 'cough and shortness of breath'),
                                                          (2, 1, 2, 'muscle pain'), (2, 1, 3, 'sore throat')]), \
        "not all options saved"
    assert Database.getAnswer(1, 1, 1) == [0], "incorrect answer saved for question 1, form 1"
    assert Database.getAnswer(1, 2, 1) == [0], "incorrect answer saved for question 2, form 1"
    assert Database.getAnswer(1, 3, 1) == "Alice Bob", "incorrect answer saved for question 3, form 1"
    visited_ids = list(map(lambda x: x[1].id, list(filter(lambda x: x[0] == "node", Database.getCurrentPositions(1)))))
    assert 2846471769152 in visited_ids, "wrong decision made"
    assert 2846471768576 not in visited_ids, "wrong decision made"
    assert all(x in Database.getTestsData() for x in [(2846471768528, "antigen test", "Nurse"),
                                                      (2846471916512, "vaccine", "Lab Technician")])
    assert Database.getTestResult(1, "Antigen Test") == "negative"
    assert 2846471916512 in visited_ids, "wrong decision made"
    assert 2846471916944 not in visited_ids, "wrong decision made"
    print("passed")


async def test_positive_for_covid():
    Database.delete_db()
    await tests_sim.run('jsons/covid example.json', 'Answers/covid_answers_positive.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert 2111561603920 in Database.getWorkflowsIds(), "workflows should contain id 2111561603920"
    assert all(x in Database.getQuestions() for x in
               [(1, 1, "If you join, you will have injections, blood draws, saliva samples, and nasal swabs of your "
                       "nose.", "one choice"),
                (1, 2, "-The most common risks are symptoms are fever, muscle aches and headaches after getting the "
                       "study vaccine. \n-There are other, less serious risks. We will tell you more about them later "
                       "in this consent form. ", "one choice"),
                (1, 3, "Full Name", "open"),
                (2, 1, "Choose your symptoms", "multi"),
                (2, 2, "Any side effect not mentioned you experienced?", "open")
                ]), "not all questions saved"
    assert all(x in Database.getQuestionnaires() for x in [(2846458731440, 1), (2846460297376, 2)]),\
        "questionnaire not saved"
    assert all(x in Database.getAnswerOptions() for x in [(1, 1, 0, 'Agree'), (1, 1, 1, 'No'), (1, 2, 0, 'Agree'),
                                                          (1, 2, 1, 'No'), (2, 1, 0, 'Fever'),
                                                          (2, 1, 1, 'cough and shortness of breath'),
                                                          (2, 1, 2, 'muscle pain'), (2, 1, 3, 'sore throat')]), \
        "not all options saved"
    assert Database.getAnswer(1, 1, 1) == [0], "incorrect answer saved for question 1, form 1"
    assert Database.getAnswer(1, 2, 1) == [0], "incorrect answer saved for question 2, form 1"
    assert Database.getAnswer(1, 3, 1) == "Alice Bob", "incorrect answer saved for question 3, form 1"
    visited_ids = list(map(lambda x: x[1].id, list(filter(lambda x: x[0] == "node", Database.getCurrentPositions(1)))))
    assert 2846471769152 in visited_ids, "wrong decision made"
    assert 2846471768576 not in visited_ids, "wrong decision made"
    assert all(x in Database.getTestsData() for x in [(2846471768528, "antigen test", "Nurse"),
                                                      (2846471916512, "vaccine", "Lab Technician")])
    assert Database.getTestResult(1, "Antigen Test") == "positive"
    assert 2846471916944 in visited_ids, "wrong decision made"
    assert 2846471916512 not in visited_ids, "wrong decision made"
    print("passed")


async def test_no_consent():
    Database.delete_db()
    await tests_sim.run('jsons/covid example.json', 'Answers/covid_answers_no_consent.json',
                        1, 'female', 20)
    assert Database.getUser(1).role == "participant", "user should be participant"
    assert Database.getUser(1).sex == "female", "user should be female"
    assert Database.getUser(1).age == 20, "user should be 20"
    assert 2111561603920 in Database.getWorkflowsIds(), "workflows should contain id 2111561603920"
    assert all(x in Database.getQuestions() for x in
               [(1, 1, "If you join, you will have injections, blood draws, saliva samples, and nasal swabs of your "
                       "nose.", "one choice"),
                (1, 2, "-The most common risks are symptoms are fever, muscle aches and headaches after getting the "
                       "study vaccine. \n-There are other, less serious risks. We will tell you more about them later "
                       "in this consent form. ", "one choice"),
                (1, 3, "Full Name", "open"),
                (2, 1, "Choose your symptoms", "multi"),
                (2, 2, "Any side effect not mentioned you experienced?", "open")
                ]), "not all questions saved"
    assert all(x in Database.getQuestionnaires() for x in [(2846458731440, 1), (2846460297376, 2)]),\
        "questionnaire not saved"
    assert all(x in Database.getAnswerOptions() for x in [(1, 1, 0, 'Agree'), (1, 1, 1, 'No'), (1, 2, 0, 'Agree'),
                                                          (1, 2, 1, 'No'), (2, 1, 0, 'Fever'),
                                                          (2, 1, 1, 'cough and shortness of breath'),
                                                          (2, 1, 2, 'muscle pain'), (2, 1, 3, 'sore throat')]), \
        "not all options saved"
    assert Database.getAnswer(1, 1, 1) == [1], "incorrect answer saved for question 1, form 1"
    assert Database.getAnswer(1, 2, 1) == [1], "incorrect answer saved for question 2, form 1"
    assert Database.getAnswer(1, 3, 1) == "Alice Bob", "incorrect answer saved for question 3, form 1"
    visited_ids = list(map(lambda x: x[1].id, list(filter(lambda x: x[0] == "node", Database.getCurrentPositions(1)))))
    assert 2846471768576 in visited_ids, "wrong decision made"
    assert 2846471769152 not in visited_ids, "wrong decision made"
    assert all(x in Database.getTestsData() for x in [(2846471768528, "antigen test", "Nurse"),
                                                      (2846471916512, "vaccine", "Lab Technician")])
    print("passed")

asyncio.run(test1())
asyncio.run(test_positive_for_covid())
asyncio.run(test_no_consent())
