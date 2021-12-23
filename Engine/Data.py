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
    #for i in range()
    print("lsls")



def get_data(participant):
    return answers[participant]
