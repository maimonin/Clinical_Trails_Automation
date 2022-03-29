def buildDALNodesFromNode(node, op_code):
    if op_code == 1:
        return DALQuestionnaire(op_code, node.id, node.title, node.number)
    elif op_code == 2:
        return DALTestNode(op_code, node.id, node.title, node.tests, node.in_charge)


def buildDALNodes(node_data):
    if node_data[0] == 1:
        return DALQuestionnaire(node_data[0], node_data[1], node_data[2], node_data[3], node_data[4])
    elif node_data[0] == 2:
        return DALTestNode(node_data[0], node_data[1], node_data[2], node_data[3], node_data[4])


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

