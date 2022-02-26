from PyQt5.QtGui import QMouseEvent
from nodeeditor.node_graphics_view import QDMGraphicsView
from nodeeditor.node_node import Node

class WFGraphicsView(QDMGraphicsView):

    def leftMouseButtonPress(self, event: QMouseEvent):
        super().leftMouseButtonPress(event)
        item = self.getItemAtClick(event)
        if hasattr(item, "node"):
            item.node.doSelect(True)
        elif item is None:
            pass