from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainterPath, QPixmap
from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_serializable import Serializable
from nodeeditor.utils import dumpException
from nodeeditor.node_socket import Socket, LEFT_BOTTOM, LEFT_CENTER, LEFT_TOP, RIGHT_BOTTOM, RIGHT_CENTER, RIGHT_TOP
from workflow_conf import OP_NODE_START, OP_NODE_FINISH, OP_NODE_QUESTIONNAIRE, OP_NODE_Test, OP_NODE_STRING, \
    OP_NODE_DECISION, OP_NODE_COMPLEX
from workflow_edge import WorkflowEdge


class WorkflowGraphicNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 210
        self.height = 70
        self.edge_size = 5
        self.edge_padding = 8

    def initAssets(self):

        # self._type_color=QColor("#0984e3")
        # self._type_font= QFont

        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._title_color = QColor("#2d3436")
        self._title_font = QFont("Ubuntu", 14)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#2d3436")
        self._color_hovered = QColor("#b2bec3")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(3.5)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(4.0)

        self._brush_title = QBrush(QColor("#2d98da"))  # node title background color
        self._brush_background = QBrush(QColor("#2d98da"))  # node header background color

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness,
                           self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness,
                             self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setBrush(Qt.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())


class WorkflowGraphicCircleThin(QDMGraphicsNode):
    @property
    def title(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return ""

    @title.setter
    def title(self, value):
        pass

    def initTitle(self):
        pass

    def initUI(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        self.initContent()

    def initSizes(self):
        super().initSizes()
        self.radius = 30
        self.width = 80
        self.height = 80

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._color = QColor("#2d3436")
        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2)

        self._brush_background_color = QColor("#2ecc71")
        self._brush_background_color.setAlpha(1)
        self._brush_background = QBrush(self._brush_background_color)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""
        # node
        painter.setPen(self._pen_default)
        painter.setBrush(self._brush_background)
        painter.drawEllipse(-self.radius, -self.radius, self.radius * 2, self.radius * 2)

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            -self.radius, -self.radius, self.radius * 2, self.radius * 2
        ).normalized()


class WorkflowGraphicCircleThick(QDMGraphicsNode):
    @property
    def title(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return ""

    @title.setter
    def title(self, value):
        pass

    def initTitle(self):
        pass

    def initUI(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        self.initContent()

    def initSizes(self):
        super().initSizes()
        self.radius = 30
        self.width = 80
        self.height = 80

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._color = QColor("#2d3436")
        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(7)

        self._brush_background_color = QColor("#2ecc71")
        self._brush_background_color.setAlpha(1)
        self._brush_background = QBrush(self._brush_background_color)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""
        # node
        painter.setPen(self._pen_default)
        painter.setBrush(self._brush_background)
        painter.drawEllipse(-self.radius, -self.radius, self.radius * 2, self.radius * 2)

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            -self.radius, -self.radius, self.radius * 2, self.radius * 2
        ).normalized()


class WorkflowGraphicSmallDiamond(QDMGraphicsNode):
    @property
    def title(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return ""

    @title.setter
    def title(self, value):
        pass

    def initTitle(self):
        pass

    def initUI(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        self.initContent()

    def initSizes(self):
        super().initSizes()
        self.width = 50
        self.height = 55

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._color = QColor("#2d3436")
        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2)

        self._color = QColor("#2d3436")
        self._pen_selected = QPen(self._color)
        self._pen_selected.setWidthF(3)

        # self._brush_background_color = QColor("#2ecc71")
        # self._brush_background = QBrush(self._brush_background_color)

        self.colors = {"yellow": QColor("#ffeaa7"), "orange": QColor("#fab1a0"),
                       "red": QColor("#ff7675"), "pink": QColor("#fd79a8"),
                       "green": QColor("#2ecc71"), "blue": QColor("#74b9ff"),
                       "grey": QColor("#ecf0f1")}

        self._brush_background = QBrush(self.colors["green"])

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""
        # node
        path_node = QPainterPath()

        path_node.setFillRule(Qt.WindingFill)
        path_node.moveTo(0, 0)
        path_node.lineTo(self.width / 2, -self.height / 2)
        path_node.lineTo(self.width, 0)
        path_node.lineTo(self.width / 2, self.height / 2)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_node.simplified())

    def change_background(self, color):
        self._brush_background = QBrush(self.colors[color])

    # def boundingRect(self) -> QRectF:
    #     """Defining Qt' bounding rectangle"""
    #     return QRectF(
    #      0,-self.height/2, self.width, self.height
    #     ).normalized()

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            0,
            -self.height / 2,
            self.width,
            self.height
        ).normalized()


class WorkflowGraphicWithIcon(QDMGraphicsNode):

    @property
    def type(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        self.type_item.setPlainText(self._type)

    @property
    def icon(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        pixmap = QPixmap(self._icon)
        self.icon_item.setPixmap(pixmap.scaled(self.icon_size, self.icon_size))

    def call_dock(self):
        self.node.emit_select_dock()

    def initUI(self):
        super().initUI()
        self.initType()
        self.initIcon()

    def initSizes(self):
        super().initSizes()
        self.edge_roundness = 20.0

        self.width = 220
        self.height = 80
        self.edge_size = 5
        self.edge_padding = 8

        self.icon_size = self.height / 3
        self.icon_circle_radius = self.icon_size

        self.icon_padding_from_perimiter = self.icon_circle_radius / 2
        self.icon_circle_horizontal_padding = self.icon_size / 3
        self.icon_circle_vertical_padding = self.height / 8

        self.type_height = self.icon_circle_vertical_padding + (1 / 8) * (
                self.height - 2 * self.icon_circle_vertical_padding)
        self.type_x = self.icon_circle_horizontal_padding * 2 + self.icon_circle_radius * 2

        self.title_height = self.icon_circle_vertical_padding + (3 / 8) * (
                self.height - 2 * self.icon_circle_vertical_padding)
        self.title_X = self.icon_circle_horizontal_padding * 2 + self.icon_circle_radius * 2

        self.type_horizontal_padding = 10
        # self.name_horizontal

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._type_color = QColor("#2d3436")
        self._type_font = QFont("Quicksand", 8)

        self._title_color = QColor("#2d3436")
        self._title_font = QFont("Quicksand", 9)
        self._title_font.setBold(True)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#2d3436")
        self._color_hovered = QColor("#b2bec3")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(1)

        self.colors = {"yellow": QColor("#ffeaa7"), "orange": QColor("#fab1a0"),
                       "red": QColor("#ff7675"), "pink": QColor("#fd79a8"),
                       "green": QColor("#55efc4"), "blue": QColor("#74b9ff"),
                       "grey": QColor("#ecf0f1")}

        self._brush_background = QBrush(self.colors["grey"])  # node header background color

        self._color_background = QColor("#C2CBCE")
        self._icon_background_brush = QBrush(self._color_background)

    def initType(self):
        """Set up the type Graphics representation: font, color, position, etc."""
        self.type_item = QGraphicsTextItem(self)
        self.type_item.node = self.node
        self.type_item.setDefaultTextColor(self._type_color)
        self.type_item.setFont(self._type_font)
        self.type_item.setPos(self.type_x, self.type_height)
        self.type_item.setTextWidth(
            self.width - self.type_x - self.type_horizontal_padding
        )

    def initTitle(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_X, self.title_height)
        self.title_item.setTextWidth(
            self.width - self.title_X - self.title_horizontal_padding
        )

    def initIcon(self):
        self.icon_item = QGraphicsPixmapItem(self)
        self.icon_item.node = self.node
        # pixmap = QPixmap(self.icon)
        # self.icon_item.setPixmap(QPixmap=pixmap)#.scaled(self.icon_size,self.icon_size))
        self.icon_item.setPos(self.icon_circle_horizontal_padding + self.icon_circle_radius / 2,
                              # + self.icon_padding_from_perimiter - self.icon_size/2,
                              self.icon_circle_vertical_padding + self.icon_circle_radius / 2)  # + self.icon_padding_from_perimiter - self.icon_size/2)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""

        # node
        path_node = QPainterPath()
        path_node.setFillRule(Qt.WindingFill)
        path_node.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen if not self.isSelected() else self._pen_selected)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_node.simplified())

        # icon's circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._icon_background_brush)
        painter.drawEllipse(self.icon_circle_horizontal_padding, self.icon_circle_vertical_padding,
                            2 * self.icon_circle_radius, 2 * self.icon_circle_radius)

    def change_background(self, color):
        self._brush_background = QBrush(self.colors[color])


class WorkflowNode(Node):
    op_icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    @property
    def type(self):
        """
        Title shown in the scene

        :getter: return current Node title
        :setter: sets Node title and passes it to Graphics Node class
        :type: ``str``
        """
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        self.grNode.type = self._type

    @property
    def icon(self):
        """
        Title shown in the scene

        :getter: return current Node title
        :setter: sets Node title and passes it to Graphics Node class
        :type: ``str``
        """
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.grNode.icon = self._icon

    def __init__(self, scene, inputs=[1], outputs=[1]):

        super().__init__(scene, f"New {self.__class__.op_title} Node", inputs, outputs)
        self.type = self.__class__.op_title
        self.icon = self.op_icon
        self.data = None

    def initInnerClasses(self):
        # self.content = WorkflowContent(self)
        self.grNode = WorkflowGraphicNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> '(x, y)':
        """
        Get the relative `x, y` position of a :class:`~nodeeditor.node_socket.Socket`. This is used for placing
        the `Graphics Sockets` on `Graphics Node`.

        :param index: Order number of the Socket. (0, 1, 2, ...)
        :type index: ``int``
        :param position: `Socket Position Constant` describing where the Socket is located. See :ref:`socket-position-constants`
        :type position: ``int``
        :param num_out_of: Total number of Sockets on this `Socket Position`
        :type num_out_of: ``int``
        :return: Position of described Socket on the `Node`
        :rtype: ``x, y``
        """
        x = self.socket_offsets[position] if (position in (LEFT_TOP, LEFT_CENTER, LEFT_BOTTOM)) else self.grNode.width + \
                                                                                                     self.socket_offsets[
                                                                                                         position]

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_roundness - index * self.socket_spacing
        elif position in (LEFT_CENTER, RIGHT_CENTER):
            num_sockets = num_out_of
            node_height = self.grNode.height
            top_offset = (self.grNode.title_height - (self.grNode.edge_roundness * 2)) / 2
            available_height = node_height - top_offset

            total_height_of_all_sockets = num_sockets * self.socket_spacing
            new_top = available_height - total_height_of_all_sockets

            # y = top_offset + index * self.socket_spacing + new_top / 2
            y = top_offset + available_height / 2.0 + (index - 0.5) * self.socket_spacing
            if num_sockets > 1:
                y -= self.socket_spacing * (num_sockets - 1) / 2

        elif position in (LEFT_TOP, RIGHT_TOP):
            # start from top
            y = self.grNode.title_height + self.grNode.title_vertical_padding + self.grNode.edge_roundness + index * self.socket_spacing
        else:
            # this should never happen
            y = 0

        return [x, y]

    def drop_action(self):
        pass

    def callback_from_window(self, content):
        pass


    def serialize(self, engine_save=False):
        try:
            res = super().serialize()
            res[
                'content'] = self.data if self.data is not None else ""
            res['op_code'] = self.__class__.op_code
            if res['op_code'] not in [OP_NODE_START, OP_NODE_FINISH]:
                res['title'] = self.type
            # remove features that is for node editor
            if engine_save:
                res = self.serialize_to_engine(res)

        except Exception as e:
            dumpException(e)

        return res

    def serialize_to_engine(self, res):
        del res['pos_x']
        del res['pos_y']

        if len(res["inputs"]) > 0:
            for idx, input in enumerate(res["inputs"]):
                del res["inputs"][idx]["index"]
                del res["inputs"][idx]["position"]
                del res["inputs"][idx]["socket_type"]
                del res["inputs"][idx]["multi_edges"]

        if len(res["outputs"]) > 0:
            for idx, output in enumerate(res["outputs"]):
                del res["outputs"][idx]["index"]
                del res["outputs"][idx]["position"]
                del res["outputs"][idx]["socket_type"]
                del res["outputs"][idx]["multi_edges"]

        if res["op_code"] == OP_NODE_START or res["op_code"] == OP_NODE_FINISH:
            del res["content"]

        elif res["op_code"] == OP_NODE_DECISION:
            for condition in res["content"]["condition"]:
                del condition["id"]
                if condition["type"] == "questionnaire condition":
                    condition["title"] = "questionnaire " + condition["title"]
                    condition["questionnaireNumber"] = int(condition["questionnaireNumber"])
                    if condition["type"] == "questionnaire condition":
                        del condition["question"]
                elif condition["type"] == "test condition":
                    condition["title"] = "test " + condition["title"]
                    if condition["satisfy"]["type"] == "range":
                        condition["satisfy"]["value"]["max"] = int(condition["satisfy"]["value"]["max"])
                        condition["satisfy"]["value"]["min"] = int(condition["satisfy"]["value"]["min"])
                elif condition["type"] == "trait condition" and condition["satisfy"]["type"] == "range":
                    condition["satisfy"]["value"]["max"] = int(condition["satisfy"]["value"]["max"])
                    condition["satisfy"]["value"]["min"] = int(condition["satisfy"]["value"]["min"])

        elif res["op_code"] == OP_NODE_QUESTIONNAIRE:
            res["content"]["questionnaire_number"] = int(res["content"]["questionnaire_number"])
            del res["content"]["node_details"]["color"]
            for question in res["content"]["questions"]:
                del question["id"]
                # remove null answers from questionnaires
                answers = question["options"]
                question["options"] = []
                for opt in answers:
                    if opt is not None:
                        question["options"].append(opt)

        elif res["op_code"] == OP_NODE_Test:
            del res["content"]["node_details"]["color"]
            for test in res["content"]["tests"]:
                del test["id"]

        elif res["op_code"] == OP_NODE_STRING:
            del res["content"]["node_details"]["color"]

        elif res["op_code"] == OP_NODE_COMPLEX:
            del res["content"]["flow"]["scene_width"]
            del res["content"]["flow"]["scene_height"]
            nodes, edges = [], []
            for node in res["content"]["flow"]["nodes"]:
                nodes.append(self.serialize_to_engine(node))
            for edge in res["content"]["flow"]["edges"]:
                edges.append(WorkflowEdge.serialize_to_engine(WorkflowEdge,edge))
            res["content"]["flow"]["nodes"] = nodes
            res["content"]["flow"]["edges"] = edges

        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        try:
            res = super().deserialize(data, hashmap, restore_id)
            self.data = data["content"]
            self.op_code = data['op_code']

            # recovering node specific attributes
            if self.op_code in [OP_NODE_QUESTIONNAIRE, OP_NODE_Test, OP_NODE_STRING]:
                self.color = data["content"]['node_details']['color']
            if self.op_code == OP_NODE_QUESTIONNAIRE:
                self.QNum = data["content"]["questionnaire_number"]
            self.get_dock_callback()(self.get_tree_build())

        except Exception as e:
            dumpException(e)
        return res

    def edit_nodes_details(self):
        pass  # To be implemented in each node

    def doSelect(self, new_state: bool = True):
        pass

    def remove(self):
        super().remove()
        self.get_dock_callback()(None)

    def emit_select_dock(self):
        pass
        self.get_dock_callback()(self.get_tree_build())

    def get_dock_callback(self):
        return self.scene.getDockCallback()

    def get_tree_build(self):
        pass

    def get_node_details(self):
        pass

    # template:
    '''   return  {
                "name": "Node Details",
                "fields": [
                    {"name": "Title", "type": "Text", "value": self.title},
                    {"name": "Time", "type": "time", "value": datetime.time(hour=1, minute=50)},
                    {"name": "Actor in charge", "type": "combobox",
                     "options": ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"], "value": "Nurse"},
                    {"name": "Actors", "type": "list",
                     "items": [{"name": "Nurse", "value": 0, "type": "spinbox"},
                               {"name": "Doctor", "value": 0, "type": "spinbox"},
                               {"name": "Participant", "value": 0, "type": "spinbox"},
                               {"name": "Investigator", "value": 0, "type": "spinbox"},
                               {"name": "Lab Technician", "value": 0, "type": "spinbox"}]},
                    {"name": "Actors", "type": "checklist",
                     "options": ["Nurse","Doctor","Participant","Investigator","Lab Technician"],
                     value:[]}
                ]}  '''
