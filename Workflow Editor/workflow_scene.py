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

    def onItemSelected(self, silent: bool = False):
        super().onItemSelected(silent)

        print(f"WorkflowScene::onItemSelected::{self.getSelectedItems()}")
        # if len(self.getSelectedItems()) > 0:
        #     self.getSelectedItems()[0].call_dock()

    def onItemsDeselected(self, silent: bool = False):
        """
        Handle Items deselection and trigger event `Items Deselected`

        :param silent: If ``True`` scene's onItemsDeselected won't be called and history stamp not stored
        :type silent: ``bool``
        """
        # somehow this event is being triggered when we start dragging file outside of our application
        # or we just loose focus on our app? -- which does not mean we've deselected item in the scene!
        # double check if the selection has actually changed, since
        current_selected_items = self.getSelectedItems()
        if current_selected_items == self._last_selected_items:
            # print("Qt itemsDeselected Invalid Event! Ignoring")
            return

        self.resetLastSelectedStates()
        if current_selected_items == []:
            self._last_selected_items = []
            if not silent:
                self.history.storeHistory("Deselected Everything")
                for callback in self._items_deselected_listeners: callback()

