def buildFromJSON(json):
    questions = []
    i = 1
    for question in json["questions"]:
        if question["type"] == "open":
            questions.append({"number": i,
                              "text": question["text"],
                              "type": "open"})
        else:
            questions.append({"number": i,
                              "text": question["text"],
                              "type": question["type"],
                              "options": question["options"]})
        i = i + 1
    return Form(json["questionnaire_number"], questions)


def formToJSON(form):
    json = {}
    json["questionnaire_number"] = form.questionnaire_number
    json["questions"] = form.questions
    return json



class Form:
    def __init__(self, questionnaire_number, questions):
        self.questionnaire_number = questionnaire_number
        self.questions = questions
