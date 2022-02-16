from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QBrush
from nodeeditor.node_graphics_scene import QDMGraphicsScene


class WFGraphicsScene (QDMGraphicsScene):

    def drawBackground(self, painter:QPainter, rect:QRect):
        """Draw background scene grid"""
        # print("WFGraphicsScene::drawBackground")
        # super().drawBackground(painter, rect)
        pass
    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        super().initAssets()
        self._color_background = QColor("#dfe6e9")


