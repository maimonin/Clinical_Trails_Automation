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
    op_icon = "assets/icons/Questionnaire-blue.png"
    op_code = OP_NODE_QUESTIONNAIRE
    op_title = "Questionnaire"
    content_label_objname = "workflow_node_questionnaire"
    QNum = "999"  # TODO : implement number generator

    def __init__(self, scene):
        super().__init__(scene)
        # @data to send to engine.
        self.data = {
            "content": {
                "node_details": {
                    "time": datetime.time(hour=0, minute=0),
                    "title": "New Questionnaire Node"
                },
                "questions": [],
                "qusetionnaire_number": self.QNum
            }
        }

    # template for questions:
    # "Multiple Choice" :{"text":"","options":[],"type":"multi"}
    # "One Choice": { "text":"","options":[],"type":"one choice"}
    # "Open": {"text":"","type":"open"}

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicWithIcon(self)

    def drop_action(self):
        if self.attributes_dock_callback is not None:
            self.attributes_dock_callback(self.get_tree_build())

    #     from Windows.questionnaire_builder import Ui_QuestionnaireBuild
    #     QuestionnaireBuild = QtWidgets.QDialog()
    #     ui = Ui_QuestionnaireBuild(lambda content: self.callback_from_window(content,QuestionnaireBuild))
    #     ui.setupUi(QuestionnaireBuild)
    #     QuestionnaireBuild.exec_()
    #     self.onDoubleClicked(self.edit_nodes_details)
    # def edit_nodes_details(self):
    #     from Windows.questionnaire_builder import Ui_QuestionnaireBuild
    #     QuestionnaireBuild = QtWidgets.QDialog()
    #     ui = Ui_QuestionnaireBuild(lambda content: self.callback_from_window(content, QuestionnaireBuild),data=self.data)
    #     ui.setupUi(QuestionnaireBuild)
    #     QuestionnaireBuild.exec_()

    # for dock build

    def doSelect(self, new_state: bool = True):
        print("WorkflowNode::doSelect")
        if new_state:
            self.attributes_dock_callback(self.get_tree_build())
        else:
            self.attributes_dock_callback(None)

    def callback_from_window(self, content):
        try:
            if content is None:
                self.remove()  # remove node
            else:
                for field in content["Node Details"]:
                    self.data["content"]["node_details"][field["name"].lower()] = field["value"]
                    if field["name"].lower() == "title":
                        self.title = field["value"]
                # TODO : implement the save of the questions and their number
                # self.data["content"]["questions"] =
                # self.data["content"]["question_number"] =

        except Exception as e:
            dumpException(e)

    def get_tree_build(self):
        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["content"]["node_details"]["title"]},
                {"name": "Time", "type": "time", "value": self.data["content"]["node_details"]["time"]}
            ],
            "Questionnaire": [
                {"name": "Questions", "type": "edit window", "value": self.data["content"]["questions"]},
                {"name": "Qusetionnaire Number", "type": "text", "value": self.data["content"]["qusetionnaire_number"]},
            ],
            "callback": self.callback_from_window
        }
        # TODO: create new window for questions creation

        return to_send


@register_node(OP_NODE_Test)
class WorkflowNode_DataEntry(WorkflowNode):
    op_icon = "assets/icons/test_blue.png"
    op_code = OP_NODE_Test
    op_title = "Test"
    content_label_objname = "workflow_node_data_entry"

    def __init__(self, scene):
        super().__init__(scene)
        # @data to send to engine.
        self.data = {
            "content": {
                "node_details": {
                    "time": datetime.time(hour=0, minute=0),
                    "title": "New Test Node",
                    "actor in charge": "Nurse"
                },
                "tests": []
            }
        }

    # template for test:
    # "Test":{"name":"", "instructions":"","staff":[],"duration": 0,"facility":""}

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicWithIcon(self)

    def doSelect(self, new_state: bool = True):
        print("WorkflowNode::doSelect")
        if new_state:
            self.attributes_dock_callback(self.get_tree_build())
        else:
            self.attributes_dock_callback(None)

    def drop_action(self):
        if self.attributes_dock_callback is not None:
            self.attributes_dock_callback(self.get_tree_build())

        # from Windows.tests_builder import Ui_Test_Builder
        # DataEntryBuild = QtWidgets.QDialog()
        # ui = Ui_Test_Builder(lambda content: self.callback_from_window(content, DataEntryBuild))
        # ui.setupUi(DataEntryBuild)
        # DataEntryBuild.exec_()

    # def edit_nodes_details(self):
    #     from Windows.tests_builder import Ui_Test_Builder
    #     DataEntryBuild = QtWidgets.QDialog()
    #     ui = Ui_Test_Builder(lambda content: self.callback_from_window(content, DataEntryBuild), data=self.data)
    #     ui.setupUi(DataEntryBuild)
    #     DataEntryBuild.exec_()

    def callback_from_window(self, content, window):
        try:
            if content is None:
                self.remove()  # remove node
            else:
                for field in content["Node Details"]:
                    self.data["content"]["node_details"][field["name"].lower()] = field["value"]
                    if field["name"].lower() == "title":
                        self.title = field["value"]
                # TODO : implement the save of the tests
                # self.data["content"]["tests"] =
        except Exception as e:
            dumpException(e)

    def get_tree_build(self):
        # TODO: create new window for tests creation
        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["content"]["node_details"]["title"]},
                {"name": "Time", "type": "time", "value": self.data["content"]["node_details"]["time"]},
                {"name": "Actor In Charge", "type": "combobox",
                 "value": self.data["content"]["node_details"]["actor in charge"],
                 "options": ["Nurse", "Doctor", "Investigator", "Lab Technician"]}
            ],
            "Tests": [
                {"name": "New Test", "type": "sub tree", "value": self.data["content"]["tests"],
                 "tree": [
                     {"name": "Name", "type": "text", "value": ""},
                     {"name": "Instructions", "type": "text", "value": ""},
                     {"name": "Staff", "type": "checklist",
                      "options": ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"],
                      "value": []},
                     {"name": "Duration", "type": "text", "value": ""},
                     {"name": "facility", "type": "text", "value": ""},
                 ],
                 "saved": []}       #TODO: implement created ones.

            ],
            "callback": self.callback_from_window
        }
        return to_send


@register_node(OP_NODE_DECISION)
class WorkflowNode_Decision(WorkflowNode):
    op_icon = "assets/icons/decision_blue.png"
    op_code = OP_NODE_DECISION
    op_title = "Decision"
    content_label_objname = "workflow_node_decision"

    def __init__(self, scene):
        super().__init__(scene)
        # @data to send to engine.
        self.data = {
            "content": {
                "node_details": {
                    "time": datetime.time(hour=0, minute=0),
                    "title": "New Decision Node"
                },
                "condition": [],
            }
        }

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicWithIcon(self)

    def doSelect(self, new_state: bool = True):
        print("WorkflowNode::doSelect")
        if new_state:
            self.attributes_dock_callback(self.get_tree_build())
        else:
            self.attributes_dock_callback(None)

    def drop_action(self):
        if self.attributes_dock_callback is not None:
            self.attributes_dock_callback(self.get_tree_build())

    #     Decision_Node = QtWidgets.QDialog()
    #     ui = Ui_Decision_Node(lambda content: self.callback_from_window(content, Decision_Node))
    #     ui.setupUi(Decision_Node)
    #     Decision_Node.exec_()
    #
    # def edit_nodes_details(self):
    #     Decision_Node = QtWidgets.QDialog()
    #     ui = Ui_Decision_Node(lambda content: self.callback_from_window(content, Decision_Node), data=self.data)
    #     ui.setupUi(Decision_Node)
    #     Decision_Node.exec_()

    def callback_from_window(self, content, window):
        try:
            if content is None:
                self.remove()  # remove node
            else:
                for field in content["Node Details"]:
                    self.data["content"]["node_details"][field["name"].lower()] = field["value"]
                    if field["name"].lower() == "title":
                        self.title = field["value"]
                # TODO implement conditions
                # self.data["content"]["condition"] =

        except Exception as e:
            dumpException(e)

    def get_tree_build(self):
        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["content"]["node_details"]["title"]},
                {"name": "Time", "type": "time", "value": self.data["content"]["node_details"]["time"]}
            ],
            "Condition": [
                # {"name": "Questions", "type": "edit window", "value": self.data["content"]["questions"]},
            ],
            "callback": self.callback_from_window
        }
        # TODO: create new window for questions creation

        return to_send


@register_node(OP_NODE_STRING)
class WorkflowNode_SimpleString(WorkflowNode):
    op_icon = "assets/icons/notificationC.png"
    op_code = OP_NODE_STRING
    op_title = "Notification"
    content_label_objname = "workflow_node_string"

    def __init__(self, scene):
        super().__init__(scene)
        # @data to send to engine.
        self.data = {
            "content": {
                "node_details": {
                    "actors": [],
                    "title": "New Notification Node"
                },
                "text": ""
            }
        }

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicWithIcon(self)

    def drop_action(self):
        if self.attributes_dock_callback is not None:
            self.attributes_dock_callback(self.get_tree_build())

    # for dock build
    def doSelect(self, new_state: bool = True):
        print("WorkflowNode::doSelect")
        if new_state:
            self.attributes_dock_callback(self.get_tree_build())
        else:
            self.attributes_dock_callback(None)

    def callback_from_window(self, content):
        try:
            if content is None:
                self.remove()  # remove node
            else:

                for field in content["Node Details"]:
                    self.data["content"]["node_details"][field["name"].lower()] = field["value"]
                    if field["name"].lower() == "title":
                        self.title = field["value"]

                self.data["content"]["text"] = content["Notification"][0]["value"]

        except Exception as e:
            dumpException(e)

    def get_tree_build(self):
        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["content"]["node_details"]["title"]},
                {"name": "Actors", "type": "checklist",
                 "options": ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"],
                 "value": self.data["content"]["node_details"]["actors"]}
            ],
            "Notification": [{"name": "Text", "type": "text", "value": self.data["content"]["text"]}],
            "callback": self.callback_from_window
        }
        return to_send


@register_node(OP_NODE_COMPLEX)
class WorkflowNode_ComplexNode(WorkflowNode):
    op_icon = "assets/icons/complex_blue2.png"
    op_code = OP_NODE_COMPLEX
    op_title = "Sub Workflow"
    content_label_objname = "workflow_node_complex"
    window = None

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicWithIcon(self)

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
