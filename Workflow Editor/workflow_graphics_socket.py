from PyQt5 import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QBrush
from nodeeditor.node_graphics_socket import QDMGraphicsSocket

RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3
class WFGraphicsSocket(QDMGraphicsSocket):
    def __init__(self, socket: 'Socket'):
        super().__init__(socket)
        self.width = 10
        if self.socket.is_input:
            self.orientation = LEFT
        else:
            self.orientation = RIGHT
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)
        # painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

        path = QPainterPath()

        painter.setRenderHint(QPainter.Antialiasing)

        if self.orientation is RIGHT:
            path.lineTo(-self.width, self.width)
            path.lineTo(-self.width, -self.width)
            path.lineTo(0, 0)

        elif self.orientation is LEFT:
            path.lineTo(0, -self.width)
            path.lineTo(self.width, 0)
            path.lineTo(0, self.width)
            path.lineTo(0, 0)
        # elif self.orientation is DOWN:
        #     path.lineTo(-self.width, self.width)
        #     path.lineTo(+self.width, +self.width)
        #     path.lineTo(0, 0)
        # elif self.orientation is UP:
        #     path.lineTo(-self.width, -self.width)
        #     path.lineTo(self.width, -self.width)
        #     path.lineTo(0, 0)

        painter.drawPath(path)

class WFGraphicsSocketDecision(WFGraphicsSocket):
    def __init__(self, socket: 'Socket'):
        super().__init__(socket)
        self.orientation = RIGHT


    def change_orientation(self,orientation):
        self.orientation = orientation
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)
        # painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

        path = QPainterPath()

        painter.setRenderHint(QPainter.Antialiasing)

        if self.orientation is RIGHT:
            path.lineTo(-self.width, self.width)
            path.lineTo(-self.width, -self.width)
            path.lineTo(0, 0)

        elif self.orientation is LEFT:
            path.lineTo(-self.width, -self.width)
            path.lineTo(self.width, -self.width)
            path.lineTo(0, 0)
        elif self.orientation is DOWN:

            painter.setBrush(Qt.Qt.NoBrush)
            painter.setPen(Qt.Qt.NoPen)
            path.lineTo(-self.width, self.width)
            path.lineTo(+self.width, self.width)
            path.lineTo(0, 0)
        elif self.orientation is UP:
            path.lineTo(-self.width, -self.width)
            path.lineTo(self.width, -self.width)
            path.lineTo(0, 0)

        painter.drawPath(path)
