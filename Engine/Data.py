import queue

from Logger import log


def init():
    global answers
    global tests
    answers = {}
    tests = {}


def add_questionnaire(results, participant):
    log("adding questionnaire of participant with id " + str(participant.id))
    message = 'participant ' + str(participant.id) + ' answers: '
    for result in results['answers']:
        message += '\n\t' + result['question']['text'] + ": " + str(result['answer'])
    log(message)
    answers[participant][results['questionnaire_number']].put(results['answers'])

def add_Form(number, participant):
    if participant in answers:
        answers[participant][number] = queue.Queue()
    else:
        ans = {number: queue.Queue()}
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

def add_test_form(name, participant):
    if participant in tests:
        tests[participant].append((name, queue.Queue()))
    else:
        ans = list()
        ans.append((name, queue.Queue()))
        tests[participant] = ans


def get_test_result(participant, test_name):
    log("getting test of " + str(participant))
    for test in reversed(tests[participant]):
        if test[0] == test_name:
            res= test[1].get(blocking=True)
            test[1].put(res)
            return res['result']
        else:
            return None



def check_data(participant, questionnaire_number, question_number, accepted_answers):
    ans = answers[participant][questionnaire_number].get(blocking=True)
    answers[participant][questionnaire_number].put(ans)
    return ans == accepted_answers
