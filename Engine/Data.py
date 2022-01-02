from Logger import log


def init():
    global answers
    global tests
    answers = {}
    tests = {}


def add_questionnaire(results, participant):
    log("adding questionnaire of " + str(participant.id))
    message = 'participant '+str(participant.id)+' answers: '
    for result in results['answers']:
        print(result)
        message += '\n\t'+result['question']['text']+": "+str(result['answer'])
    log(message)
    if participant in answers:
        answers[participant][results['qusetionnaire_number']] = results['answers']
    else:
        ans = {results['qusetionnaire_number']: results['answers']}
        answers[participant] = ans


def add_test(name, results, participant):
    log("adding test of " + str(participant))
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


def check_data(participant, questionnaireNumber, questionNumber, acceptedAnswers):
    ans = answers[participant][questionnaireNumber][questionNumber - 1]['answer']
    return ans == acceptedAnswers
