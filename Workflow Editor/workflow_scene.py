import json
import os
from collections import OrderedDict

from nodeeditor.node_graphics_scene import QDMGraphicsScene
from nodeeditor.node_scene import Scene, InvalidFile
from nodeeditor.utils import dumpException

from workflow_edge import WorkflowEdge
from workflow_graphics_scene import WFGraphicsScene


class WorkflowScene(Scene):
    def __init__(self):
        super().__init__()
        self.dockCallback = lambda x: x  # dull function so it won't crash in any case

    def addAttributesDockCallback(self, callback):
        self.dockCallback = callback

    def initUI(self):
        self.grScene = WFGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def getEdgeClass(self):
        """Return the class representing Edge. Override me if needed"""
        return WorkflowEdge

    def pass_to_attribute_dock(self, data):
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

    def saveToFile(self, filename: str):
        """
        Save this `Scene` to the file on disk.

        :param filename: where to save this scene
        :type filename: ``str``
        """
        filename_split = filename.split(".")
        if len(filename_split) == 2:
            editor_file = filename_split[0] + ".editor." + filename_split[1]
            engine_file = filename_split[0] + ".engine." + filename_split[1]
        elif len(filename_split) == 3 and (filename_split[1] == "editor" or filename_split[1] == "engine" ):
            editor_file = filename
            engine_file = filename_split[0] + ".engine." + filename_split[2]
        else:
            print("Invalid file name")
            return

        # save for editor
        with open(editor_file, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
            print("saving to", editor_file, "was successful.")

            self.has_been_modified = False
            self.filename = filename

        # save for engine
        with open(engine_file, "w") as file:
            file.write(json.dumps(self.serialize(True), indent=4))
            print("saving to", engine_file, "was successful.")

            self.has_been_modified = False

    def loadFromFile(self, filename: str):
        """
        Load `Scene` from a file on disk

        :param filename: from what file to load the `Scene`
        :type filename: ``str``
        :raises: :class:`~nodeeditor.node_scene.InvalidFile` if there was an error decoding JSON file
        """
        filename_split = filename.split(".")
        if len(filename_split) != 3 or filename_split[1] != "editor":
            print("Invalid file name")
            return

        with open(filename, "r") as file:
            raw_data = file.read()
            try:
                raw_data = raw_data.encode('utf-8')
                data = json.loads(raw_data)
                self.filename = filename
                # FIXME: need to add "attributes_dock_callback to edge deserialization
                self.deserialize(data)
                self.has_been_modified = False
            except json.JSONDecodeError:
                raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                dumpException(e)

    def serialize(self, engine_save=False) -> OrderedDict:
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize(engine_save))
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])
