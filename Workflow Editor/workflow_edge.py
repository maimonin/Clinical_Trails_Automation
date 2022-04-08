from nodeeditor.node_edge import Edge, EDGE_TYPE_DIRECT
from nodeeditor.utils import dumpException

from workflow_graphics_edge import WFGraphicsEdgeText, WFGraphicsRegularEdgeWithText

NORMAL = 0
RELATIVE = 1
FIXED = 2


class WorkflowEdge(Edge):
    attributes_dock_callback = None

    def __init__(self, scene: 'Scene', start_socket: 'Socket' = None, end_socket: 'Socket' = None,
                 edge_type=EDGE_TYPE_DIRECT, text="No Node", attributes_dock_callback=None):
        self._text = text
        super().__init__(scene, start_socket, end_socket, edge_type)
        self.data = {
            "content": {
                "edge_details": {
                    "title": "",
                    "type": NORMAL,
                    "min": "",
                    "max": ""
                },
                "callback": self.callback_from_dock,

            }}
        self.text = text
        # self.attributes_dock_callback = attributes_dock_callback

    @property
    def text(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.grEdge.text = self._text

    def set_attributes_dock_callback(self, callback):
        self.attributes_dock_callback = callback

    def getGraphicsEdgeClass(self):
        """Returns the class representing Graphics Edge"""
        return WFGraphicsRegularEdgeWithText

    def doSelect(self, new_state: bool = True):
        try:
            if new_state:
                self.attributes_dock_callback(self.get_tree_build())
            else:
                self.attributes_dock_callback(None)
        except Exception as e:
            dumpException(e)

    def callback_from_dock(self, content):
        try:
            for field in content["Edge Details"]:
                # self.data["content"]["edge_details"][field["name"].lower()] = field["value"]
                if field["name"].lower() == "title":
                    self.text = field["value"]
        except Exception as e:
            dumpException(e)

    def get_tree_build(self):
        to_send = {
            "Edge Details": [
                {"name": "Title", "type": "text", "value": self.data["content"]["edge_details"]["title"]},
                {"name": "Accepted Delay", "type": "tree", "items": [
                    {"name": "Min", "type": "text", "value": self.data["content"]["edge_details"]["min"], "placeholder": "Enter Min Delay"},
                    {"name": "Max", "type": "text", "value": self.data["content"]["edge_details"]["max"], "placeholder": "Enter Max Delay"}
                ]}
            ],
            "callback": self.callback_from_dock
        }
        return to_send
