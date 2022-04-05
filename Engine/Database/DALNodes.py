def buildDALNodesFromNode(node, op_code):
    if op_code == 1:
        return DALQuestionnaire(op_code, node.id, node.title, node.number)
    elif op_code == 2:
        return DALTestNode(op_code, node.id, node.title, node.tests, node.in_charge)
    elif op_code == 3:
        return DALDecision(op_code, node.id, node.title, node.conditions)
    elif op_code == 4:
        return DALStringNode(op_code, node.id, node.title, node.text, node.actors)


def buildDALNodes(node_data):
    if node_data[0] == 1:
        return DALQuestionnaire(node_data[0], node_data[1], node_data[2], node_data[3], node_data[4])
    elif node_data[0] == 2:
        return DALTestNode(node_data[0], node_data[1], node_data[2], node_data[3], node_data[4])
    elif node_data[0] == 3:
        return DALDecision(node_data[0], node_data[1], node_data[2], condJSON(node_data[3], node_data[4], node_data[5]))
    elif node_data[0] == 4:
        return DALStringNode(node_data[0], node_data[1], node_data[2], node_data[3], node_data[4])
    elif node_data[0] == 6:
        return DALComplexNode(node_data[0], node_data[1], node_data[2], node_data[3])


def condJSON(quest_conditions, test_conditions, trait_conditions):
    conditions = []
    for cond in quest_conditions:
        # convert string list of accepted answers from database to integer list
        answers = list(map(int, cond[4][1:len(cond[4])-1].split(',')))
        conditions.append({
            "title": cond[1],
            "type": "questionnaire condition",
            "questionnaireNumber": cond[2],
            "questionNumber": cond[3],
            "acceptedAnswers": answers
        })
    for cond in test_conditions:
        if cond[3] == "one_choice":
            conditions.append({
                "title": cond[1],
                "type": "test condition",
                "test": cond[2],
                "satisfy": {
                    "type": "one_choice",
                    "value": cond[4]
                }
            })
        else:
            conditions.append({
                "title": cond[1],
                "type": "test condition",
                "test": cond[2],
                "satisfy": {
                    "type": "range",
                    "value": {
                        "min": cond[5],
                        "max": cond[6]
                    }
                }
            })
    for cond in trait_conditions:
        if cond[3] == "one_choice":
            conditions.append({
                "title": cond[1],
                "type": "trait condition    ",
                "test": cond[2],
                "satisfy": {
                    "type": "one_choice",
                    "value": cond[4]
                }
            })
        else:
            conditions.append({
                "title": cond[1],
                "type": "trait condition    ",
                "test": cond[2],
                "satisfy": {
                    "type": "range",
                    "value": {
                        "min": cond[5],
                        "max": cond[6]
                    }
                }
            })
    return conditions


class DALQuestionnaire:
    def __init__(self, op_code, node_id, title, form, form_id):
        self.op_code = op_code
        self.id = node_id
        self.title = title
        self.form = form
        self.form_id = form_id


class DALTestNode:
    def __init__(self, op_code, node_id, title, tests, in_charge):
        self.op_code = op_code
        self.id = node_id
        self.title = title
        self.tests = tests
        self.in_charge = in_charge


class DALDecision:
    def __init__(self, op_code, node_id, title, conditions):
        self.op_code =  op_code
        self.id = node_id
        self.title = title
        self.conditions = conditions


class DALStringNode:
    def __init__(self, op_code, node_id, title, text, actors):
        self.op_code = op_code
        self.id = node_id
        self.title = title
        self.text = text
        lower_actors = []
        for actor in actors:
            lower_actors.append(str(actor).lower())
        self.actors = lower_actors


class DALComplexNode:
    def __init__(self, op_code, node_id, title, flow):
        self.op_code = op_code
        self.id = node_id
        self.title = title
        self.flow = flow
