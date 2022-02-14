import threading

from Logger import log
from user_lists import get_participant


def init():
    global answers
    global tests
    answers = {}
    tests = {}


def add_questionnaire(results, id):
    participant=get_participant(id)
    log("adding questionnaire of participant with id " + str(participant.id))
    message = 'participant ' + str(participant.id) + ' answers: '
    for result in results['answers']:
        message += '\n\t' + result['question']['text'] + ": " + str(result['answer'])
    log(message)
    if participant in answers:
        cond=answers[participant][results['questionnaire_number']]
        answers[participant][results['questionnaire_number']] = results['answers']
        cond.notify_all()
    else:
        ans = {results['questionnaire_number']: results['answers']}
        answers[participant] = ans

def add_form(results, participant):
    if participant in answers:
        answers[participant][results['questionnaire_number']] = threading.Condition()
    else:
        ans = {results['questionnaire_number']: threading.Condition()}
        answers[participant] = ans


def add_test(name, results, participant):
    log('participant ' + str(participant.id) + ' results of test ' + results['test'] + ": " + str(results['result']))
    print(results)
    if participant in tests:
        tests[participant].append((name, results))
    else:
        ans = list()
        ans.append((name, results))
        tests[participant] = ans


def get_test_result(participant, test_name):
    log("getting test of " + str(participant))
    for test in reversed(tests[participant]):
        if test[0] == test_name:
            return test[1]['result']
        else:
            return None


def get_data(participant):
    return answers[participant]


def check_data(participant, questionnaire_number, question_number, accepted_answers):
    while isinstance(answers[participant][questionnaire_number], threading.Condition()):
        answers[participant][questionnaire_number].wait()
    ans = answers[participant][questionnaire_number][question_number - 1]['answer']
    return ans == accepted_answers
