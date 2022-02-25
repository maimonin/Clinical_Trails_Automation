import datetime
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from qtpy import QtCore

from Windows.decisionNode.win_deciosionNode import Ui_Decision_Node
from Windows.string_node import Ui_string_node
from workflow_conf import *
from workflow_node_base import *
from nodeeditor.utils import dumpException


class WorkflowInputContent(QDMNodeContentWidget):
    def __init__(self, node, callback):
        super().__init__(node)
        self.callback = callback

    def initUI(self):
        self.edit = QLineEdit("", self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.textChanged.connect(lambda: self.callback(self.edit.text()))
        # self.edit.changeEvent()

        # callback(self.edit.text())


class WorkflowTimeInputContent(QDMNodeContentWidget):
    def __init__(self, node, callback):
        super().__init__(node)
        self.callback = callback

    def initUI(self):
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFixedHeight(300)
        self.groupBox.setFixedWidth(100)
        self.edit_second = QtWidgets.QLineEdit(self.groupBox)
        self.edit_second.setPlaceholderText('seconds')
        self.edit_second.setObjectName(self.node.content_label_objname + '_seconds')
        self.edit_second.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.edit_minutes = QtWidgets.QLineEdit(self.groupBox)
        self.edit_minutes.setGeometry(QtCore.QRect(0, 30, 100, 30))
        self.edit_minutes.setObjectName(self.node.content_label_objname + '_minutes')
        self.edit_minutes.setPlaceholderText('minutes')
        self.edit_hours = QtWidgets.QLineEdit(self.groupBox)
        self.edit_hours.setGeometry(QtCore.QRect(0, 60, 100, 30))
        self.edit_hours.setObjectName(self.node.content_label_objname + '_hours')
        self.edit_hours.setPlaceholderText('hours')
        self.edit_hours.textChanged.connect(
            lambda: self.callback(self.edit_second.text(), self.edit_minutes.text(), self.edit_hours.text()))
        self.edit_minutes.textChanged.connect(
            lambda: self.callback(self.edit_second.text(), self.edit_minutes.text(), self.edit_hours.text()))
        self.edit_second.textChanged.connect(
            lambda: self.callback(self.edit_second.text(), self.edit_minutes.text(), self.edit_hours.text()))
        # self.edit.changeEvent()

        # callback(self.edit.text())


@register_node(OP_NODE_QUESTIONNAIRE)
class WorkflowNode_Questionnaire(WorkflowNode):
    icon = "assets/icons/Questionnaire-blue.png"
    op_code = OP_NODE_QUESTIONNAIRE
    op_title = "Questionnaire"
    content_label_objname = "workflow_node_questionnaire"

    def initInnerClasses(self):
        self.content = WorkflowContent_with_button(self, )
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode_wide(self)

    def drop_action(self):
        from Windows.questionnaire_builder import Ui_QuestionnaireBuild
        QuestionnaireBuild = QtWidgets.QDialog()
        ui = Ui_QuestionnaireBuild(lambda content: self.callback_from_window(content, QuestionnaireBuild))
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
        ui = Ui_QuestionnaireBuild(lambda content: self.callback_from_window(content, QuestionnaireBuild),
                                   data=self.data)
        ui.setupUi(QuestionnaireBuild)
        QuestionnaireBuild.exec_()


@register_node(OP_NODE_Test)
class WorkflowNode_DataEntry(WorkflowNode):
    icon = "assets/icons/test_blue.png"
    op_code = OP_NODE_Test
    op_title = "Test"
    content_label_objname = "workflow_node_data_entry"

    def initInnerClasses(self):
        self.content = WorkflowContent_with_button(self, )
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode(self)

    def drop_action(self):
        from Windows.tests_builder import Ui_Test_Builder
        DataEntryBuild = QtWidgets.QDialog()
        ui = Ui_Test_Builder(lambda content: self.callback_from_window(content, DataEntryBuild))
        ui.setupUi(DataEntryBuild)
        DataEntryBuild.exec_()

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
        from Windows.tests_builder import Ui_Test_Builder
        DataEntryBuild = QtWidgets.QDialog()
        ui = Ui_Test_Builder(lambda content: self.callback_from_window(content, DataEntryBuild), data=self.data)
        ui.setupUi(DataEntryBuild)
        DataEntryBuild.exec_()


@register_node(OP_NODE_DECISION)
class WorkflowNode_Decision(WorkflowNode):
    icon = "assets/icons/decision_blue.png"
    op_code = OP_NODE_DECISION
    op_title = "Decision"
    content_label_objname = "workflow_node_decision"

    def initInnerClasses(self):
        self.content = WorkflowContent_with_button(self, )
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode(self)

    def drop_action(self):
        Decision_Node = QtWidgets.QDialog()
        ui = Ui_Decision_Node(lambda content: self.callback_from_window(content, Decision_Node))
        ui.setupUi(Decision_Node)
        Decision_Node.exec_()

    def edit_nodes_details(self):
        Decision_Node = QtWidgets.QDialog()
        ui = Ui_Decision_Node(lambda content: self.callback_from_window(content, Decision_Node), data=self.data)
        ui.setupUi(Decision_Node)
        Decision_Node.exec_()

    def callback_from_window(self, content, window):
        try:
            window.close()
            if content is None:
                self.remove()  # remove node
            else:
                self.data = content
        except Exception as e:
            dumpException(e)


@register_node(OP_NODE_STRING)
class WorkflowNode_SimpleString(WorkflowNode):
    icon = "assets/icons/notificationC.png"
    op_code = OP_NODE_STRING
    op_title = "Notification"
    content_label_objname = "workflow_node_string"

    def initInnerClasses(self):
        self.content = WorkflowContent_with_button(self, )
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode(self)

    def save_data_when_changed(self, text):
        self.data = text

    def drop_action(self):
        # String_Node = QtWidgets.QDialog()
        # ui = Ui_string_node(lambda content: self.callback_from_window(content, String_Node))
        # ui.setupUi(String_Node)
        # String_Node.exec_()
        to_send = {
            "sections": [{
                "name": "Node Details",
                "fields": [
                    {"name": "Title", "type": "Text", "value": ""},
                    {"name": "Time", "type": "time", "value": datetime.time(hour=1, minute=50)},
                    {"name": "Actor in charge", "type": "combobox",
                     "options": ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"], "value": "Nurse"},
                    {"name": "Actors", "type": "list",
                     "items": [{"name": "Nurse", "value": 0, "type": "spinbox"},
                               {"name": "Doctor", "value": 0, "type": "spinbox"},
                               {"name": "Participant", "value": 0, "type": "spinbox"},
                               {"name": "Investigator", "value": 0, "type": "spinbox"},
                               {"name": "Lab Technician", "value": 0, "type": "spinbox"}]}
                ]},
                {
                    "name": "Notification",
                    "fields": [
                        {"name": "Text", "type": "Text", "value": ""}
                    ]
                }

            ],
            "callback": self.callback_from_window("")
        }

        if self.attributes_dock_callback is not None:
            self.attributes_dock_callback(to_send)

    def callback_from_window(self, content):
        try:
            if content is None:
                self.remove()  # remove node
            else:
                self.data = content
        except Exception as e:
            dumpException(e)

    def callback_to_window(self):

        pass

    def edit_nodes_details(self):
        String_Node = QtWidgets.QDialog()
        ui = Ui_string_node(lambda content: self.callback_from_window(content, String_Node), data=self.data)
        ui.setupUi(String_Node)
        String_Node.exec_()


# @register_node(OP_NODE_TIME_CONSTRAINT)
# class WorkflowNode_TimeConstraint(WorkflowNode):
#     icon = "icons/time.png"
#     op_code = OP_NODE_TIME_CONSTRAINT
#     op_title = "Time Constraint"
#     content_label_objname = "workflow_node_time_constraint"
#
#     def initInnerClasses(self):
#         self.content = WorkflowTimeInputContent(self, self.save_data_when_changed)
#         self.grNode = WorkflowGraphicNode_long(self)
#         self.data = {"type" : "time","Hours": 0,"Minutes": 0,"Seconds": 0}
#
#
#     def save_data_when_changed(self, Seconds,Minutes,Hours):
#         try:
#             Hours = int(Hours)
#         except:
#             Hours=0
#         try:
#             Minutes = int(Minutes)
#         except:
#             Minutes = 0
#         try:
#             Seconds = int(Seconds)
#         except:
#             Seconds = 0
#         self.data = {"type" : "time","Hours": Hours,"Minutes": Minutes,"Seconds": Seconds}


@register_node(OP_NODE_COMPLEX)
class WorkflowNode_ComplexNode(WorkflowNode):
    icon = "assets/icons/complex_blue2.png"
    op_code = OP_NODE_COMPLEX
    op_title = "Sub Workflow"
    content_label_objname = "workflow_node_complex"
    window = None

    def initInnerClasses(self):
        self.content = WorkflowContent_with_button(self, )
        self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicNode(self)

    def save_data_when_changed(self, text):
        self.data = text

    def drop_action(self):
        from workflow_complex_window import Workflow_Complex_Window
        self.window = Workflow_Complex_Window(lambda flow_json: self.callback_from_window(flow_json))
        self.window.show()

    def callback_from_window(self, content):
        try:
            self.window.close()
            if content is None:
                self.remove()
            else:
                self.data = {"type": "complex", "flow": content}
            self.window = None
        except Exception as e:
            dumpException(e)

    def edit_nodes_details(self):
        try:
            from workflow_complex_window import Workflow_Complex_Window
            self.window = Workflow_Complex_Window(lambda flow_json: self.callback_from_window(flow_json),
                                                  data=self.data["flow"], name="Subflow")
            # self.window.load_data()
            self.window.show()
        except Exception as e:
            dumpException(e)
