from PyQt5.QtCore import *
from workflow_conf import *
from workflow_node_base import *




class WorkflowInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit= QLineEdit("String",self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

@register_node(OP_NODE_STRING)
class WorkflowNode_SimpleString(WorkflowNode):
    icon = "images/str.png"
    op_code = OP_NODE_STRING
    op_title = "Simple String"
    content_label_objname = "workflow_node_string"

    def initInnerClasses(self):
        self.content=WorkflowInputContent(self)
        self.grNode = WorkflowGraphicNode(self)
# @register_node(OP_NODE_STRING)
# class WorkflowNode_Decision(WorkflowNode):
#     icon = "images/descision.png"
#     op_code = OP_NODE_STRING
#     op_title = "Simple String"
#     content_label_objname = "workflow_node_string"
#
#     def initInnerClasses(self):
#         self.content=WorkflowInputContent(self)
#         self.grNode = WorkflowGraphicNode(self)