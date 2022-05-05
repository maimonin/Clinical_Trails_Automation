import datetime
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from nodeeditor.node_socket import LEFT_BOTTOM, RIGHT_TOP, LEFT_CENTER, LEFT_TOP, RIGHT_BOTTOM, RIGHT_CENTER
from qtpy import QtCore

from workflow_conf import *
from workflow_node_base import *
from nodeeditor.utils import dumpException
from workflow_graphics_socket import WFGraphicsSocketDecision, WFGraphicsSocket


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

    def __init__(self, scene):
        super().__init__(scene)
        self.color = "Grey"
        self.QNum = str(scene.getNextQuestionnaireNumber())
        # @data to send to engine.
        self.data = {
                "node_details": {
                    "time": QTime.toString(QTime(0, 0)),
                    "title": "New Questionnaire Node",
                    "color": self.color
                },
                "questions": [],
                "questionnaire_number": self.QNum
            }


    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicWithIcon(self)

    def drop_action(self):
        if self.attributes_dock_callback is not None:
            self.attributes_dock_callback(self.get_tree_build())

    def doSelect(self, new_state: bool = True):
        try:
            if new_state:
                self.attributes_dock_callback(self.get_tree_build())
            else:
                self.attributes_dock_callback(None)
        except Exception as e:
            dumpException(e)

    def callback_from_window(self, content):
        try:
            if content is None:
                self.remove()  # remove node
            else:
                self.data["node_details"]["title"] = content["Node Details"][0]["value"]
                self.title = content["Node Details"][0]["value"]
                self.data["node_details"]["time"] = content["Node Details"][1]["value"].toString()
                self.data["node_details"]["color"] = content["Node Details"][2]["value"]
                self.color = content["Node Details"][2]["value"]
                self.grNode.change_background(content["Node Details"][2]["value"].lower())
                self.data["questions"] = []
                self.data["questions"] = content["Content"][1]["value"]
                self.data["questionnaire_number"] = content["Content"][0]["value"]
                self.QNum = content["Content"][0]["value"]

        except Exception as e:
            dumpException(e)

    def get_tree_build(self):
        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["node_details"]["title"]},
                {"name": "Time", "type": "time",
                 "value": QTime.fromString(self.data["node_details"]["time"])},
                {"name": "Color", "type": "combobox icons", "value": self.color,
                 "options": ["Grey", "Yellow", "Orange", "Red", "Pink", "Green", "Blue"]}
            ],
            "Content": [
                {"name": "Questionnaire #", "type": "text", "value": self.data["questionnaire_number"]},
                {"name": "Questions", "type": "q sub tree", "value": self.data["questions"]}
            ],
            "callback": self.callback_from_window
        }
        return to_send

    def export_to_UI(self, export):
        result = []
        for item in export:
            name = list(item.keys())[0]

            if name == "Multiple Choice":
                type_idx = 1
            elif name == "One Choice":
                type_idx = 2
            elif name == "Open":
                type_idx = 3

            if type_idx != 3:
                result.append(
                    {"name": name, "type": type_idx, "text": item[name]["text"], "sub": item[name]["options"]})
            else:
                result.append(
                    {"name": name, "type": type_idx, "text": item[name]["text"]})

        return result

    def remove(self):
        super().remove()
        for node in self.scene.nodes:
            if node.op_code == OP_NODE_DECISION:
                node.data["condition"] = [condition for condition in node.data["condition"] if self.QNum != condition["questionnaireNumber"]]



@register_node(OP_NODE_Test)
class WorkflowNode_DataEntry(WorkflowNode):
    op_icon = "assets/icons/test_blue.png"
    op_code = OP_NODE_Test
    op_title = "Test"
    content_label_objname = "workflow_node_data_entry"

    def __init__(self, scene):
        super().__init__(scene)
        self.color = "Grey"
        # @data to send to engine.
        self.data = {
                "node_details": {
                    "time": QTime.toString(QTime(0, 0)),
                    "title": "New Test Node",
                    "actor in charge": "Nurse",
                    "color": self.color
                },
                "tests": []
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

    def callback_from_window(self, content):
        try:
            if content is None:
                self.remove()  # remove node
            else:
                for field in content["Node Details"]:
                    self.data["node_details"][field["name"].lower()] = field["value"]
                    if field["name"].lower() == "title":
                        self.title = field["value"]
                    if field["name"].lower() == "color":
                        self.grNode.change_background(field["value"].lower())
                        self.color = field["value"]
                    if field["name"].lower() == "time":
                        self.data["node_details"][field["name"].lower()] = field["value"].toString()

                self.data["tests"] = []
                for test in content["Content"][0]["value"]:
                    self.data["tests"].append(test)

        except Exception as e:
            dumpException(e)

    def get_tree_build(self):

        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["node_details"]["title"]},
                {"name": "Time", "type": "time",
                 "value": QTime.fromString(self.data["node_details"]["time"])},
                {"name": "Actor In Charge", "type": "combobox",
                 "value": self.data["node_details"]["actor in charge"],
                 "options": ["Nurse", "Doctor", "Investigator", "Lab Technician"]},
                {"name": "Color", "type": "combobox icons", "value": self.color,
                 "options": ["Grey", "Yellow", "Orange", "Red", "Pink", "Green", "Blue"]}
            ],
            "Content": [
                {"name": "Tests", "type": "test sub tree", "value": self.data["tests"]}],
            "callback": self.callback_from_window
        }
        return to_send

    def remove(self):
        super().remove()
        # TODO update all decisions to remove.


@register_node(OP_NODE_DECISION)
class WorkflowNode_Decision(WorkflowNode):
    op_icon = "assets/icons/decision_blue.png"
    op_code = OP_NODE_DECISION
    op_title = "Decision"
    content_label_objname = "workflow_node_decision"

    def __init__(self, scene, inputs=[1], outputs=[4, 2]):
        self.scene = scene
        super().__init__(scene, inputs, outputs)
        # self.color = "Green"
        # @data to send to engine.
        self.data = {
                "node_details": {
                    "time": QTime.toString(QTime(0, 0)),
                    "title": "New Decision Node",
                    # "color": self.color
                },
                "condition": [],
            }

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicSmallDiamond(self)

    def doSelect(self, new_state: bool = True):
        print("WorkflowNode::doSelect")
        if new_state:
            self.attributes_dock_callback(self.get_tree_build())
        else:
            self.attributes_dock_callback(None)

    def drop_action(self):
        if self.attributes_dock_callback is not None:
            self.attributes_dock_callback(self.get_tree_build())

    def callback_from_window(self, content):
        try:
            if content is None:
                self.remove()  # remove node
            else:
                for field in content["Node Details"]:
                    self.data["node_details"][field["name"].lower()] = field["value"]
                    if field["name"].lower() == "title":
                        self.title = field["value"]
                    # if field["name"].lower() == "color":
                    #     self.grNode.change_background(field["value"].lower())
                    #     self.color = field["value"]
                    if field["name"].lower() == "time":
                        self.data["node_details"][field["name"].lower()] = field["value"].toString()
                self.data["condition"] = []
                for condition in content["Condition"][0]["value"]:
                    self.data["condition"].append(condition)

        except Exception as e:
            dumpException(e)

    def initSettings(self):
        """Initialize properties and socket information"""

        self.socket_spacing = 22
        TOP = 7
        DOWN = 8
        self.input_socket_position = 7  # Top - new position we creates
        self.output_socket_position_good = RIGHT_CENTER
        self.output_socket_position_bad = 8

        self.input_multi_edged = False
        self.output_multi_edged = True
        self.socket_offsets = {
            LEFT_CENTER: 0,
            RIGHT_CENTER: 0,
            TOP: 0
        }

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """
        Create sockets for inputs and outputs

        :param inputs: list of Socket Types (int)
        :type inputs: ``list``
        :param outputs: list of Socket Types (int)
        :type outputs: ``list``
        :param reset: if ``True`` destroys and removes old `Sockets`
        :type reset: ``bool``
        """
        Socket.Socket_GR_Class = WFGraphicsSocketDecision
        if reset:
            # clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # remove grSockets from scene
                for socket in (self.inputs + self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs = []
                self.outputs = []

        # create new sockets
        counter = 0
        for item in inputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.input_socket_position,
                socket_type=item, multi_edges=self.input_multi_edged,
                count_on_this_node_side=len(inputs), is_input=True
            )
            counter += 1
            self.inputs.append(socket)
            socket.grSocket.change_orientation(2)
        counter = 0
        # bad socket
        bad_socket = self.__class__.Socket_class(
            node=self, index=counter, position=self.output_socket_position_bad,
            socket_type=outputs[0], multi_edges=self.output_multi_edged,
            count_on_this_node_side=len(outputs), is_input=False
        )
        try:
            bad_socket.grSocket.change_orientation(1)

            self.outputs.append(bad_socket)
        except Exception as e:
            dumpException(e)
        good_socket = self.__class__.Socket_class(
            node=self, index=counter, position=self.output_socket_position_good,
            socket_type=outputs[1], multi_edges=self.output_multi_edged,
            count_on_this_node_side=len(outputs), is_input=False
        )
        self.outputs.append(good_socket)
        Socket.Socket = WFGraphicsSocket

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> '(x, y)':
        """
        return the only position for this node: on the right of this node
        """
        x = 0 if (position == LEFT_CENTER) else self.grNode.width if position == RIGHT_CENTER else self.grNode.width / 2
        y = 0 if position in (
            LEFT_CENTER, RIGHT_CENTER) else -self.grNode.height / 2 if position == 7 else self.grNode.height / 2

        return [x, y]

    def get_tree_build(self):
        nodes_content = self.get_nodes_from_scene()

        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["node_details"]["title"]},
                {"name": "Time", "type": "time",
                 "value": QTime.fromString(self.data["node_details"]["time"])},
                # {"name": "Color", "type": "combobox icons", "value": self.color,
                #  "options": ["Grey", "Yellow", "Orange", "Red", "Pink", "Green", "Blue"]}
            ],
            "Condition": [
                {"name": "Conditions", "type": "cond sub tree", "value": self.data["condition"], "known": nodes_content},
            ],
            "callback": self.callback_from_window
        }

        return to_send

    def get_nodes_from_scene(self):
        nodes_content = []

        for node in self.scene.nodes:
            if node.op_code == OP_NODE_QUESTIONNAIRE:
                new_questions = []
                for question in node.data["questions"]:
                    if question["type"] != "open":
                        new_questions.append({"type": question["type"], "question": question["text"], "answers": question["options"]})
                nodes_content.append(
                    {"node": OP_NODE_QUESTIONNAIRE, "content": {"id": node.QNum, "questions": new_questions}})
            elif node.op_code == OP_NODE_Test:
                tests_names = []
                for test in node.data["tests"]:
                    nodes_content.append({"node": OP_NODE_Test, "content": test["name"]})

        return nodes_content


@register_node(OP_NODE_STRING)
class WorkflowNode_SimpleString(WorkflowNode):
    op_icon = "assets/icons/notificationC.png"
    op_code = OP_NODE_STRING
    op_title = "Notification"
    content_label_objname = "workflow_node_string"

    def __init__(self, scene):
        super().__init__(scene)
        self.color = "Grey"
        # @data to send to engine.
        self.data = {
                "node_details": {
                    "actors": [],
                    "title": "New Notification Node",
                    "color": self.color
                },
                "text": ""
            }

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicWithIcon(self)

    def save_data_when_changed(self, text):
        self.data = text

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
                    self.data["node_details"][field["name"].lower()] = field["value"]
                    if field["name"].lower() == "title":
                        self.title = field["value"]
                    if field["name"].lower() == "color":
                        self.grNode.change_background(field["value"].lower())
                        self.color = field["value"]

                self.data["text"] = content["Notification"][0]["value"]

        except Exception as e:
            dumpException(e)

    def get_tree_build(self):
        to_send = {
            "Node Details": [
                {"name": "Title", "type": "text", "value": self.data["node_details"]["title"]},
                {"name": "Actors", "type": "checklist",
                 "options": ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"],
                 "value": self.data["node_details"]["actors"]},
                {"name": "Color", "type": "combobox icons", "value": self.color,
                 "options": ["Grey", "Yellow", "Orange", "Red", "Pink", "Green", "Blue"]}
            ],
            "Notification": [{"name": "Text", "type": "text", "value": self.data["text"]}],
            "callback": self.callback_from_window
        }
        return to_send


@register_node(OP_NODE_START)
class WorkflowNode_Start(WorkflowNode):
    op_icon = ""
    op_code = OP_NODE_START
    op_title = "Start"
    content_label_objname = "workflow_node_start"

    def __init__(self, scene, inputs=[], outputs=[2]):
        super().__init__(scene, inputs, outputs)

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicCircleThin(self)

    def drop_action(self):
        pass

    def callback_from_window(self, content, window):
        pass

    def initSettings(self):
        """Initialize properties and socket information"""
        self.socket_spacing = 22

        self.output_socket_position = RIGHT_CENTER
        self.output_multi_edged = True
        self.socket_offsets = {
            LEFT_BOTTOM: -1,
            LEFT_CENTER: -1,
            LEFT_TOP: -1,
            RIGHT_BOTTOM: 1,
            RIGHT_CENTER: 1,
            RIGHT_TOP: 1,
        }

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """
        Create sockets for inputs and outputs

        :param inputs: list of Socket Types (int)
        :type inputs: ``list``
        :param outputs: list of Socket Types (int)
        :type outputs: ``list``
        :param reset: if ``True`` destroys and removes old `Sockets`
        :type reset: ``bool``
        """

        if reset:
            # clear old sockets
            if hasattr(self, 'outputs'):
                # remove grSockets from scene
                for socket in (self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.outputs = []

        # create new sockets

        counter = 0
        for item in outputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position,
                socket_type=item, multi_edges=self.output_multi_edged,
                count_on_this_node_side=len(outputs), is_input=False
            )
            counter += 1
            self.outputs.append(socket)

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> '(x, y)':
        """
        return the only position for this node: on the right of this node
        """
        x = self.grNode.radius
        y = 0

        return [x, y]

    # Override the remove method. ( it cant be removed)
    # unless called from a new file
    def remove(self, new_file=False):
        if new_file:
            super().remove()


@register_node(OP_NODE_FINISH)
class WorkflowNode_Finish(WorkflowNode):
    op_icon = ""
    op_code = OP_NODE_FINISH
    op_title = "Finish"
    content_label_objname = "workflow_node_finish"

    def __init__(self, scene, inputs=[2], outputs=[]):
        super().__init__(scene, inputs, outputs)

    def initInnerClasses(self):
        # self.content = WorkflowContent_with_button(self, )
        # self.content.connect_callback(self.edit_nodes_details)
        self.grNode = WorkflowGraphicCircleThick(self)

    def drop_action(self):
        pass

    def edit_nodes_details(self):
        pass

    def callback_from_window(self, content, window):
        pass

    def initSettings(self):
        """Initialize properties and socket information"""
        self.socket_spacing = 22

        self.input_socket_position = LEFT_CENTER
        self.input_multi_edged = True
        self.socket_offsets = {
            LEFT_BOTTOM: -1,
            LEFT_CENTER: -1,
            LEFT_TOP: -1,
            RIGHT_BOTTOM: 1,
            RIGHT_CENTER: 1,
            RIGHT_TOP: 1,
        }

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """
        Create sockets for inputs and outputs

        :param inputs: list of Socket Types (int)
        :type inputs: ``list``
        :param outputs: list of Socket Types (int)
        :type outputs: ``list``
        :param reset: if ``True`` destroys and removes old `Sockets`
        :type reset: ``bool``
        """

        if reset:
            # clear old sockets
            if hasattr(self, 'inputs'):
                # remove grSockets from scene
                for socket in (self.inputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs = []

        # create new sockets

        counter = 0
        for item in inputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.input_socket_position,
                socket_type=item, multi_edges=self.input_multi_edged,
                count_on_this_node_side=len(inputs), is_input=True
            )
            counter += 1
            self.inputs.append(socket)

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> '(x, y)':
        """
        return the only position for this node: on the right of this node
        """
        x = -self.grNode.radius
        y = 0

        return [x, y]

    # Override the remove method. ( it cant be removed)
    # unless called from a new file
    def remove(self, new_file=False):
        if new_file:
            super().remove()


@register_node(OP_NODE_COMPLEX)
class WorkflowNode_ComplexNode(WorkflowNode):
    op_icon = "assets/icons/complex_blue2.png"
    op_code = OP_NODE_COMPLEX
    op_title = "Sub Workflow"
    content_label_objname = "workflow_node_complex"
    window = None

    # FIXME: sub workflow override the dock callback to all nodes.

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
