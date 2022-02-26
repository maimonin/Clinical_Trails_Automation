from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_serializable import Serializable
from nodeeditor.utils import dumpException


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


class WorkflowGraphicNodeQuicksand(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 320
        self.height = 80
        self.edge_size = 5
        self.edge_padding = 8
        self.icon_horizontal_padding = 20
        self.icon_vertical_padding = 20

        self.type_height = self.icon_vertical_padding +  (1/8) * (self.height -  2*self.icon_vertical_padding)
        self.name_height =  self.icon_vertical_padding +  (5/8) * (self.height -  2*self.icon_vertical_padding)

        self.type_horizontal_padding = 5
        self.name_horizontal
    def initAssets(self):

        # self._type_color=QColor("#0984e3")
        # self._type_font= QFont



        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._title_color = QColor("#2d3436")
        self._title_font = QFont("Quicksand", 14)

        self._type_color = QColor("#2d3436")
        self._type_font = QFont("Quicksand", 14)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#2d3436")
        self._color_hovered = QColor("#b2bec3")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(3.5)


        self._brush_background = QBrush(QColor("#ecf0f1"))  # node hea
        # der background color
    def initType(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._type_color)
        self.title_item.setFont(self._type_font)
        self.title_item.setPos(self.title_horizontal_padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self.type_horizontal_padding
        )
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""



        #node
        path_node = QPainterPath()
        path_node.setFillRule(Qt.WindingFill)
        path_node.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_node.simplified())




class WorkflowGraphicWithIcon(QDMGraphicsNode):
    pass

class WorkflowGraphicNode_wide(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 300
        self.height = 100
        self.edge_size = 5
        self.edge_padding = 8


class WorkflowGraphicNode_long(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 150
        self.edge_size = 5
        self.edge_padding = 8


class WorkflowContent_with_button(QDMNodeContentWidget):
    def initUI(self):
        pass
        # button=QPushButton("Edit",self)
        # self.btn=button

    def connect_callback(self, callback):
        # self.btn.clicked.connect(callback)
        pass


class WorkflowContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel("", self)
        button = QPushButton("raviv", self)


class WorkflowNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    def __init__(self, scene, inputs=[1], outputs=[1]):

        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.data = None
        self.attributes_dock_callback = None

    def initInnerClasses(self):
        self.content = WorkflowContent(self)
        self.grNode = WorkflowGraphicNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True

    def drop_action(self):
        pass

    def callback_from_window(self, content):
        pass

    def set_attributes_dock_callback(self, callback):
        self.attributes_dock_callback = callback

    def serialize(self):
        try:
            res = super().serialize()
            # ser_content = self.content.serialize() if isinstance(self.content, Serializable) else {}

            res[
                'content'] = self.data if self.data is not None else ""  # changed it from content to data due to issues,Raviv.
            res['op_code'] = self.__class__.op_code
        except Exception as e:
            dumpException(e)
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        self.data = data['content']
        self.op_code = data['op_code']
        # print("Deserialized node base '%s'" % self.__class__.__name__, "res:", res)
        return res

    def edit_nodes_details(self):
        pass  # To be implemented in each node
