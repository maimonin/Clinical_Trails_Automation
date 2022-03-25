class Form:
    def __init__(self, questionnaire_number, questions):
        self.questionnaire_number = questionnaire_number
        self.questions = questions

    def __init__(self, json):
        self.questionnaire_id = json["questionnaire_number"]
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
        self.questions = questions
