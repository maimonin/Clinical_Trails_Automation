def buildDALNodesFromNode(node, op_code):
    if op_code == 1:
        return DALQuestionnaire(op_code, node.id, node.title, node.number)


def buildDALNodes(node_data):
    if node_data[0] == 1:
        return DALQuestionnaire(node_data[0], node_data[1], node_data[2], node_data[3], node_data[4])


class DALQuestionnaire:
    def __init__(self, op_code, node_id, title, form, form_id):
        self.op_code = op_code
        self.id = node_id
        self.title = title
        self.form = form
        self.form_id = form_id

