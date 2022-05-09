from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QFont, QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem
from nodeeditor.node_edge import Edge
from nodeeditor.node_graphics_edge import QDMGraphicsEdge
from qtpy import QtCore


class WFGraphicsEdgeText(QGraphicsItem):

        def __init__(self ,edge:Edge,parent:QWidget = None):
            """
            :param node: reference to :class:`~nodeeditor.node_node.Node`
            :type node: :class:`~nodeeditor.node_node.Node`
            :param parent: parent widget
            :type parent: QWidget

            :Instance Attributes:

                - **node** - reference to :class:`~nodeeditor.node_node.Node`
            """
            super().__init__(parent)
            self.edge = edge

            self.posSource = [0, 0]
            self.posDestination = [200, 100]
            # init our flags
            self._was_moved = False
            self._last_selected_state = False

            self.initSizes()
            self.initAssets()
            self.initUI()


        @property
        def text(self):
            """title of this `Edge`

            :getter: current Graphics Edge title
            :setter: stores and make visible the new title
            :type: str
            """
            return self._text

        @text.setter
        def text(self, value):
            self._text = value
            self.text_item.setPlainText(self._text)

        def initUI(self):
            """Set up this ``QGraphicsItem``"""

            # self.setFlag(QGraphicsItem.ItemIsMovable)
            self.setAcceptHoverEvents(True)

            # init title
            self.initText()
            self.text = self.edge.text


        def initSizes(self):
            """Set up internal attributes like `width`, `height`, etc."""
            self.width = 60
            self.height = 20

            self.text_horizontal_padding = 4.0

        def initAssets(self):
            self._text_color = Qt.black
            self._text_font = QFont("Ubuntu", 10)

        def setSource(self, x: float, y: float):
            """ Set source point

            :param x: x position
            :type x: ``float``
            :param y: y position
            :type y: ``float``
            """
            self.posSource = [x, y]

        def setDestination(self, x: float, y: float):
            """ Set destination point

            :param x: x position
            :type x: ``float``
            :param y: y position
            :type y: ``float``
            """
            self.posDestination = [x, y]
        def boundingRect(self) -> QRectF:
            """Defining Qt' bounding rectangle"""
            return QRectF(
                0,
                0,
                self.width,
                self.height
            ).normalized()

        def initText(self):
            """Set up the title Graphics representation: font, color, position, etc."""
            self.text_item = QGraphicsTextItem(self)
            return
            self.text_item.edge = self.edge
            self.text_item.setDefaultTextColor(self._text_color)
            self.text_item.setFont(self._text_font)
            self.text_item.setPos(self.text_horizontal_padding, 0)
            self.text_item.setTextWidth(
                self.width
                - 2 * self.text_horizontal_padding
            )

        def update(self, rect: QtCore.QRectF = ...) -> None:
            self.setPos(self.posSource[0] + ((self.posDestination[0]-self.posSource[0])/2),self.posSource[1] + ((self.posDestination[1]-self.posSource[1])/2))

        def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
            pass


class WFGraphicsRegularEdgeWithText(QDMGraphicsEdge):
    def __init__(self, edge:'Edge', parent:QWidget = None):
        self.text_item = None

        super().__init__(edge,parent)

    def initUI(self):
        super().initUI()
        self.initTitle()

    @property
    def text(self):
        """title of this `Edge`

        :getter: current Graphics Edge title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        # if self.text_item is not None:
        self.text_item.setPlainText(self._text)

    def initAssets(self):
        super().initAssets()
        self._title_color = Qt.black
        self._title_font = QFont("Ubuntu", 10)

    def initTitle(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.text_item = QGraphicsTextItem(self)
        self.text_item.setFlag(QGraphicsItem.ItemIsMovable)
        # self.title_item.node = self.edge
        self.text_item.setDefaultTextColor(self._title_color)
        self.text_item.setFont(self._title_font)
        # print(self.pos().x())
        self.text_item.setPos(self.pos().x(), 0)
        self.text_item.setTextWidth(
            200
        )

    def update_text_item(self):
        self.text_item.setPos(self.posSource[0] + ((self.posDestination[0] - self.posSource[0]) / 2), self.posSource[1] + ((self.posDestination[1] - self.posSource[1]) / 2))

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Qt's overridden method to paint this Graphics Edge. Path calculated
            in :func:`~nodeeditor.node_graphics_edge.QDMGraphicsEdge.calcPath` method"""
        self.setPath(self.calcPath())

        self.update_text_item()
        if self.hovered and self.edge.end_socket is not None:

            painter.setPen(self._pen_hovered)
            painter.drawPath(self.path())

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        if self.isSelected():
            # print("selected")
            pass
        painter.drawPath(self.path())

