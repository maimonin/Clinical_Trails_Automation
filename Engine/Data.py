import asyncio
from datetime import datetime

from Database import Database
from Logger import log


def init():
    global answers
    global tests
    answers = {}
    tests = {}


def add_questionnaire(results, participant):
    log("adding questionnaire of participant with id " + str(participant))
    message = 'participant ' + str(participant) + ' answers: '
    i = 0
    for result in results['answers']:
        message += '\n\t' + result['question']['text'] + ": " + str(result['answer'])
        Database.addAnswer(results['questionnaire_number'], i, participant, datetime.now(), str(result['answer']))
        i = i + 1
    log(message)
    event = answers[participant][results['questionnaire_number']]
    event.set()


def add_form(number, participant):
    if participant in answers:
        answers[participant][number] = asyncio.Event()
    else:
        ans = {number: asyncio.Event()}
        answers[participant] = ans


def add_test(name, results, participant):
    log('participant ' + str(participant) + ' results of test ' + results['test'] + ": " + str(results['result']))
    Database.addTestResults(name, participant, datetime.now(), results['result'])
    for test in reversed(tests[participant]):
        if test[0] == name:
            event = test[1]
            event.set()


def add_test_form(name, participant):
    if participant in tests:
        tests[participant].append((name, asyncio.Event()))
    else:
        ans = list()
        ans.append((name, asyncio.Event()))
        tests[participant] = ans


async def get_test_result(participant_id, test_name):
    log("getting results of test " + test_name + " of participant " + str(participant_id))
    for test in reversed(tests[participant_id]):
        if test[0] == test_name:
            await test[1].wait()
            print("im here")
    return Database.getTestResult(participant_id, test_name)


async def parse_questionnaire_condition(patient, questionnaire_number, question_number, accepted_answers):
    return await check_data(patient, questionnaire_number, question_number, accepted_answers)


def parse_trait_condition(participant_id, satisfy, trait):
    participant = Database.getUser(participant_id)
    if satisfy['type'] == 'range':
        values = satisfy['value']
        return True if values['min'] <= participant.get_traits()[trait] <= values['max'] else False
    else:
        return True if participant.get_traits()[trait] == satisfy['value'] else False


async def parse_test_condition(patient, satisfy, test_name):
    print(satisfy)
    if satisfy['type'] == 'range':
        values = satisfy['value']
        print(values)
        return True if values['min'] <= int(await get_test_result(patient, test_name)) <= values['max'] else False
    else:
        print('hola')
        return True if await get_test_result(patient, test_name) == satisfy['value'] else False


async def check_data(participant, questionnaire_number, question_number, accepted_answers):
    if questionnaire_number in answers[participant]:
        await answers[participant][questionnaire_number].wait()
    ans = Database.getAnswer(questionnaire_number, question_number, participant)
    return ans == accepted_answers
