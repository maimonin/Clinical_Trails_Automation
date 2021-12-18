from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode



class WorkflowGraphicNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_size = 5
        self.edge_padding=8


class WorkflowContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel("", self)

class WorkflowNode(Node):
    icon=""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"
    def __init__(self, scene,inputs=[1],outputs=[1]) :

        super().__init__(scene,self.__class__.op_title,inputs,outputs)

    def initInnerClasses(self):
        self.content = WorkflowContent(self)
        self.grNode = WorkflowGraphicNode(self)
