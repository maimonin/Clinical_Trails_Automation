from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from workflow_conf import *
from workflow_node_base import *
from nodeeditor.utils import dumpException


class WorkflowInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit= QLineEdit("String",self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

@register_node(OP_NODE_QUESTIONNAIRE)
class WorkflowNode_Questionnaire(WorkflowNode):
    icon = "images/Questionnaire-icon.png"
    op_code = OP_NODE_QUESTIONNAIRE
    op_title = "Questionnaire"
    content_label_objname = "workflow_node_questionnaire"

    def initInnerClasses(self):
        # self.content=WorkflowInputContent(self)
        self.grNode = WorkflowGraphicNode(self)
    def drop_action(self):
        from Windows.questionnaire_builder import Ui_QuestionnaireBuild
        QuestionnaireBuild = QtWidgets.QDialog()
        ui = Ui_QuestionnaireBuild(lambda content: self.callback_from_window(content,QuestionnaireBuild))
        ui.setupUi(QuestionnaireBuild)
        QuestionnaireBuild.exec_()

    def callback_from_window(self, content, window):
        window.close()
        if content is None:
            self.remove()
        else:
            self.content = content

@register_node(OP_NODE_DATA_ENTRY)
class WorkflowNode_DataEntry(WorkflowNode):
    icon = "images/data_entry.png"
    op_code = OP_NODE_DATA_ENTRY
    op_title = "Data Entry"
    content_label_objname = "workflow_node_data_entry"

    def initInnerClasses(self):
        # self.content=WorkflowInputContent(self)
        self.grNode = WorkflowGraphicNode(self)
    def drop_action(self):
        from Windows.tests_builder import Ui_Test_Builder
        DataEntryBuild = QtWidgets.QDialog()
        ui = Ui_Test_Builder(lambda content: self.callback_from_window(content,DataEntryBuild))
        ui.setupUi(DataEntryBuild)
        DataEntryBuild.exec_()

    def callback_from_window(self,content,window):
        try:
            window.close()
            if content is None:
                self.remove() #  remove node
            else:
                print(content)
                self.content=content
        except Exception as e : dumpException(e)
# @register_node(OP_NODE_STRING)
# class WorkflowNode_SimpleString(WorkflowNode):
#     icon = "images/str.png"
#     op_code = OP_NODE_STRING
#     op_title = "Simple String"
#     content_label_objname = "workflow_node_string"
#
#     def initInnerClasses(self):
#         self.content=WorkflowInputContent(self)
#         self.grNode = WorkflowGraphicNode(self)
#     def set_content(self,content):
#         self.content=content
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