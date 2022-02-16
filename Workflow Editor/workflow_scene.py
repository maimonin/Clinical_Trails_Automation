from nodeeditor.node_graphics_scene import QDMGraphicsScene
from nodeeditor.node_scene import Scene

from workflow_graphics_scene import WFGraphicsScene


class WorkflowScene(Scene):
    def initUI(self):
        self.grScene = WFGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)
