from PyQt5.QtGui import QMouseEvent
from nodeeditor.node_graphics_view import QDMGraphicsView
from nodeeditor.node_node import Node

from workflow_edge_intersect import WorkflowEdgeIntersect


class WFGraphicsView(QDMGraphicsView):
    def __init__(self, grScene: 'QDMGraphicsScene', parent: 'QWidget'=None):
        super().__init__(grScene,parent)
        self.edgeIntersect = WorkflowEdgeIntersect(self)

    def leftMouseButtonPress(self, event: QMouseEvent):
        super().leftMouseButtonPress(event)
        item = self.getItemAtClick(event)
        if hasattr(item, "node"):
            item.node.doSelect(True)
        if hasattr(item, "edge"):
            item.edge.doSelect(True)
        elif item is None:
            self.grScene.scene.pass_to_attribute_dock(None)
            pass