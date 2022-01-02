from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_serializable import Serializable
from nodeeditor.utils import dumpException


class WorkflowGraphicNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 70
        self.edge_size = 5
        self.edge_padding=8


class WorkflowGraphicNode_wide(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 100
        self.edge_size = 5
        self.edge_padding=8
class WorkflowContent_with_button(QDMNodeContentWidget):
    def initUI(self):
        button=QPushButton("Edit",self)
        self.btn=button
    def connect_callback(self,callback):
        self.btn.clicked.connect(callback)

class WorkflowContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel("", self)
        button=QPushButton("raviv",self)


class WorkflowNode(Node):
    icon=""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"
    def __init__(self, scene,inputs=[1],outputs=[1]) :

        super().__init__(scene,self.__class__.op_title,inputs,outputs)
        self.data = None
    def initInnerClasses(self):
        self.content = WorkflowContent(self)
        self.grNode = WorkflowGraphicNode(self)
    def initSettings(self):
        super().initSettings()
        self.input_multi_edged= True
    def drop_action(self):
        pass
    def callback_from_window(self, content, window):
        pass

    def serialize(self):
        try:
            res = super().serialize()
            # ser_content = self.content.serialize() if isinstance(self.content, Serializable) else {}

            res['content']=self.data if self.data is not None else "" # changed it from content to data due to issues,Raviv.
            res['op_code'] = self.__class__.op_code
        except Exception as e: dumpException(e)
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        self.data = data['content']
        self.op_code=data['op_code']
        # print("Deserialized node base '%s'" % self.__class__.__name__, "res:", res)
        return res

    def edit_nodes_details(self):
        pass # To be implemented in each node