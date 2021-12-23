answers = {}
tests = {}


def add_questionnaire(results, participant):
    if participant in answers:
        answers[participant].append(results)
    else:
        ans = list()
        ans.append(results)
        answers[participant] = ans


def add_test(name, results, participant):
    if participant in tests:
        tests[participant].append((name, results))
    else:
        ans = list()
        ans.append((name, results))
        tests[participant] = ans


def get_test_result(participant, test_name):
    for test in reversed(tests[participant]):
        if test[0] == test_name:
            return test[1]
        else:
            return None


def get_data(participant):
    return answers[participant]
