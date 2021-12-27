from PyQt5 import QtWidgets
from PyQt5.QtCore import *

from Windows.decisionNode.win_deciosionNode import Ui_Decision_Node
from Windows.string_node import Ui_string_node
from workflow_conf import *
from workflow_node_base import *
from nodeeditor.utils import dumpException


class WorkflowInputContent(QDMNodeContentWidget):
    def __init__(self, node, callback):
        super().__init__(node)
        self.callback=callback
    def initUI(self):
        self.edit= QLineEdit("",self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.textChanged.connect( lambda: self.callback(self.edit.text()))
        # self.edit.changeEvent()

        #callback(self.edit.text())

@register_node(OP_NODE_QUESTIONNAIRE)
class WorkflowNode_Questionnaire(WorkflowNode):
    icon = "images/Questionnaire-icon.png"
    op_code = OP_NODE_QUESTIONNAIRE
    op_title = "Questionnaire"
    content_label_objname = "workflow_node_questionnaire"

    def initInnerClasses(self):
        self.content=WorkflowContent_with_button(self,)
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode_wide(self)
    def drop_action(self):
        from Windows.questionnaire_builder import Ui_QuestionnaireBuild
        QuestionnaireBuild = QtWidgets.QDialog()
        ui = Ui_QuestionnaireBuild(lambda content: self.callback_from_window(content,QuestionnaireBuild))
        ui.setupUi(QuestionnaireBuild)
        QuestionnaireBuild.exec_()
        self.onDoubleClicked(self.edit_nodes_details)

        # self.
    def callback_from_window(self, content, window):
        print(content)
        window.close()
        if content is None:
            self.remove()

        else:
            self.data = content
    def edit_nodes_details(self):
        from Windows.questionnaire_builder import Ui_QuestionnaireBuild
        QuestionnaireBuild = QtWidgets.QDialog()
        ui = Ui_QuestionnaireBuild(lambda content: self.callback_from_window(content, QuestionnaireBuild),data=self.data)
        ui.setupUi(QuestionnaireBuild)
        QuestionnaireBuild.exec_()
@register_node(OP_NODE_DATA_ENTRY)
class WorkflowNode_DataEntry(WorkflowNode):
    icon = "images/data_entry.png"
    op_code = OP_NODE_DATA_ENTRY
    op_title = "Data Entry"
    content_label_objname = "workflow_node_data_entry"

    def initInnerClasses(self):
        self.content=WorkflowContent_with_button(self,)
        self.content.connect_callback(self.edit_nodes_details)
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
                self.data=content
        except Exception as e : dumpException(e)
    def edit_nodes_details(self):
        from Windows.tests_builder import Ui_Test_Builder
        DataEntryBuild = QtWidgets.QDialog()
        ui = Ui_Test_Builder(lambda content: self.callback_from_window(content,DataEntryBuild),data=self.data)
        ui.setupUi(DataEntryBuild)
        DataEntryBuild.exec_()
@register_node(OP_NODE_DECISION)
class WorkflowNode_Decision(WorkflowNode):
    icon = "images/decision.png"
    op_code = OP_NODE_DECISION
    op_title = "Decision"
    content_label_objname = "workflow_node_decision"

    def initInnerClasses(self):
        self.content = WorkflowContent_with_button(self, )
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode(self)

    def drop_action(self):
        Decision_Node = QtWidgets.QDialog()
        ui = Ui_Decision_Node(lambda content: self.callback_from_window(content,Decision_Node))
        ui.setupUi(Decision_Node)
        Decision_Node.exec_()

    def edit_nodes_details(self):
        Decision_Node = QtWidgets.QDialog()
        ui = Ui_Decision_Node(lambda content: self.callback_from_window(content,Decision_Node),data=self.data)
        ui.setupUi(Decision_Node)
        Decision_Node.exec_()

    def callback_from_window(self,content,window):
        try:
            window.close()
            if content is None:
                self.remove() #  remove node
            else:
                self.data = content
        except Exception as e : dumpException(e)

@register_node(OP_NODE_STRING)
class WorkflowNode_SimpleString(WorkflowNode):
    icon = "images/str.png"
    op_code = OP_NODE_STRING
    op_title = "Simple String"
    content_label_objname = "workflow_node_string"

    def initInnerClasses(self):
        self.content = WorkflowContent_with_button(self, )
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode(self)

    def save_data_when_changed(self, text):
        self.data = text

    def drop_action(self):
        String_Node = QtWidgets.QDialog()
        ui = Ui_string_node(lambda content: self.callback_from_window(content, String_Node))
        ui.setupUi(String_Node)
        String_Node.exec_()

    def callback_from_window(self, content, window):
        try:
            window.close()
            if content is None:
                self.remove()  # remove node
            else:
                self.data = content
        except Exception as e:
            dumpException(e)

    def edit_nodes_details(self):
        String_Node = QtWidgets.QDialog()
        ui = Ui_string_node(lambda content: self.callback_from_window(content,String_Node),data=self.data)
        ui.setupUi(String_Node)
        String_Node.exec_()


@register_node(OP_NODE_TIME_CONSTRAINT)
class WorkflowNode_TimeConstraint(WorkflowNode):
    icon = "images/time.png"
    op_code = OP_NODE_TIME_CONSTRAINT
    op_title = "Time Constraint"
    content_label_objname = "workflow_node_time_constraint"

    def initInnerClasses(self):
        self.content = WorkflowInputContent(self, self.save_data_when_changed)
        self.grNode = WorkflowGraphicNode(self)
        self.data = "String"


    def save_data_when_changed(self, text):
        # TODO check for correct input - 0 as default
        # TODO change to dict by inbar request
        self.data = text

    # TODO keep implement
    # def drop_action(self):
    #     Time_constraint_node = QtWidgets.QDialog()
    #     ui = Ui_string_node(lambda content: self.callback_from_window(content, Time_constraint_node))
    #     ui.setupUi(Time_constraint_node)
    #     Time_constraint_node.exec_()
    #
    # def callback_from_window(self, content, window):
    #     try:
    #         window.close()
    #         if content is None:
    #             self.remove()  # remove node
    #         else:
    #             self.data = content
    #     except Exception as e:
    #         dumpException(e)

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