from Logger import log


def init():
    global answers
    global tests
    answers = {}
    tests = {}


def add_questionnaire(results, participant):
    log("adding questionnaire of " + str(participant.id))
    message = 'participant ' + str(participant.id) + ' answers: '
    for result in results['answers']:
        message += '\n\t' + result['question']['text'] + ": " + str(result['answer'])
    log(message)
    if participant in answers:
        answers[participant][results['questionnaire_number']] = results['answers']
    else:
        ans = {results['questionnaire_number']: results['answers']}
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
    ans = answers[participant][questionnaire_number][question_number - 1]['answer']
    return ans == accepted_answers
