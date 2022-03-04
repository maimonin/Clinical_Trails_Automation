from nodeeditor.node_graphics_scene import QDMGraphicsScene
from nodeeditor.node_scene import Scene

from workflow_graphics_scene import WFGraphicsScene


class WorkflowScene(Scene):
    def __init__(self):
        super().__init__()
        self.dockCallback=lambda x:x #dull function so it won't crash in any case

    def addAttributesDockCallback(self,callback):
        self.dockCallback=callback
    def initUI(self):
        self.grScene = WFGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)
    def pass_to_attribute_dock(self,data):
        self.dockCallback(data)