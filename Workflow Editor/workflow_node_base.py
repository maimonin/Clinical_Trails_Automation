from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainterPath, QPixmap
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



    def initUI(self):
        super().initUI()
        self.initType()
        self.initIcon()
    def initSizes(self):


        super().initSizes()
        self.edge_roundness = 20.0

        self.width = 400
        self.height = 120
        self.edge_size = 5
        self.edge_padding = 8

        self.icon_size = self.height / 3
        self.icon_circle_radius = self.icon_size

        self.icon_padding_from_perimiter = self.icon_circle_radius/2
        self.icon_circle_horizontal_padding = self.icon_size / 3
        self.icon_circle_vertical_padding = self.height / 8

        self.type_height = self.icon_circle_vertical_padding + (1 / 8) * (self.height - 2 * self.icon_circle_vertical_padding)
        self.type_x = self.icon_circle_horizontal_padding * 2 + self.icon_circle_radius * 2

        self.title_height = self.icon_circle_vertical_padding + (3 / 8) * (self.height - 2 * self.icon_circle_vertical_padding)
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


        self._brush_background = QBrush(QColor("#ecf0f1"))  # node hea
        # der background color

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
        self.icon_item.setPos(self.icon_circle_horizontal_padding + self.icon_circle_radius / 2,#+ self.icon_padding_from_perimiter - self.icon_size/2,
                              self.icon_circle_vertical_padding +  self.icon_circle_radius / 2) #+ self.icon_padding_from_perimiter - self.icon_size/2)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""



        #node
        path_node = QPainterPath()
        path_node.setFillRule(Qt.WindingFill)
        path_node.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen if not self.isSelected() else self._pen_selected)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_node.simplified())

        #icon's circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._icon_background_brush)
        painter.drawEllipse(self.icon_circle_horizontal_padding, self.icon_circle_vertical_padding, 2 * self.icon_circle_radius, 2 * self.icon_circle_radius)









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

        super().__init__(scene,f"New {self.__class__.op_title} Node" , inputs, outputs)
        self.type=self.__class__.op_title
        self.icon=self.op_icon
        self.data = None
        self.attributes_dock_callback = None

    def initInnerClasses(self):
        # self.content = WorkflowContent(self)
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

    def doSelect(self, new_state: bool=True):
        pass