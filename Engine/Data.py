answers = {}
tests = {}


def add_data(results, participant):
    if participant in answers:
        answers[participant].append(results)
    else:
        ans = list()
        ans.append(results)
        answers[participant] = ans


def get_data(participant):
    return answers[participant]
