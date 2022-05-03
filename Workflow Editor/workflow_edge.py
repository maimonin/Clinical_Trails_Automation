from collections import OrderedDict
from nodeeditor.node_edge import Edge, EDGE_TYPE_DIRECT
from nodeeditor.utils import dumpException
from workflow_graphics_edge import WFGraphicsEdgeText, WFGraphicsRegularEdgeWithText
from PyQt5.QtCore import QTime

NORMAL = 0
RELATIVE = 1


class WorkflowEdge(Edge):
    attributes_dock_callback = None

    def __init__(self, scene: 'Scene', start_socket: 'Socket' = None, end_socket: 'Socket' = None,
                 edge_type=EDGE_TYPE_DIRECT, text="No Title", attributes_dock_callback=None):
        self._text = text
        super().__init__(scene, start_socket, end_socket, edge_type)
        # data for engine
        self.data = {
            "content": {
                "edge_details": {
                    "title": "",
                    "min": {"Hours": "00", "Minutes": "00", "Seconds": "00"},
                    "max": {"Hours": "00", "Minutes": "00", "Seconds": "00"},
                },
                "callback": self.callback_from_dock,

            }}
        self.text = text
        self.type = NORMAL
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
        self.grEdge.text = self.text
        try:
            if new_state:
                self.attributes_dock_callback(self.get_tree_build())
            else:
                self.attributes_dock_callback(None)
        except Exception as e:
            dumpException(e)

    def callback_from_dock(self, content):
        try:
            input_title = content["Edge Details"][0]["value"]
            input_min = QTime.toString(content["Edge Details"][1]["items"][0]["value"])
            input_max = QTime.toString(content["Edge Details"][1]["items"][1]["value"])
            self.update_label(input_title, input_min, input_max)

            self.type = NORMAL if (input_min == "" or input_max == "") else RELATIVE

            self.data["content"]["edge_details"]["title"] = input_title
            if input_min != "":
                self.data["content"]["edge_details"]["min"]["Hours"] = input_min[:2]
                self.data["content"]["edge_details"]["min"]["Minutes"] = input_min[3:5]
                self.data["content"]["edge_details"]["min"]["Seconds"] = input_min[6:]
            if input_max != "":
                self.data["content"]["edge_details"]["max"]["Hours"] = input_max[:2]
                self.data["content"]["edge_details"]["max"]["Minutes"] = input_max[3:5]
                self.data["content"]["edge_details"]["max"]["Seconds"] = input_max[6:]
        except Exception as e:
            dumpException(e)

    def update_label(self, input_title, input_min, input_max):
        if input_title == "":
            self.text = "No Title"
            if input_min != "" and input_max != "":
                self.text += " : " + input_min + " - " + input_max
        else:
            self.text = input_title
            if input_min != "" and input_max != "":
                self.text += " : " + input_min + " - " + input_max

    def get_tree_build(self):
        to_send = {
            "Edge Details": [
                {"name": "Title", "type": "text", "value": self.data["content"]["edge_details"]["title"]},
                {"name": "Accepted Delay", "type": "tree", "items": [
                    {"name": "Min", "type": "time",
                     "value": self.convert_to_time(self.data["content"]["edge_details"]["min"]),
                     "placeholder": "Enter Min Delay", "format": "hh:mm:ss"},
                    {"name": "Max", "type": "time",
                     "value": self.convert_to_time(self.data["content"]["edge_details"]["max"]),
                     "placeholder": "Enter Max Delay", "format": "hh:mm:ss"}
                ]}
            ],
            "callback": self.callback_from_dock
        }
        return to_send

    def convert_to_time(self, time_dict):
        dict_to_string = time_dict["Hours"] + ":" + time_dict["Minutes"] + ":" + time_dict["Seconds"]
        result = QTime.fromString(dict_to_string, "hh:mm:ss")
        return result

    def serialize(self, engine_save=False) -> OrderedDict:
        if self.type == NORMAL:
            result = OrderedDict([
                ('id', self.id),
                ('start', self.start_socket.id if self.start_socket is not None else None),
                ('end', self.end_socket.id if self.end_socket is not None else None),
                ('type', self.type),
                ('edge_type', self.edge_type)
            ])
        elif self.type == RELATIVE:
            result = OrderedDict([
                ('id', self.id),
                ('type', self.type),
                ('start', self.start_socket.id if self.start_socket is not None else None),
                ('end', self.end_socket.id if self.end_socket is not None else None),
                ('content', self.data['content']['edge_details']),
                ('edge_type', self.edge_type)
            ])
        if engine_save:
            del result["edge_type"]
        return result

    def deserialize(self, data: dict, hashmap: dict = {}, restore_id: bool = True, *args, **kwargs) -> bool:
        if restore_id: self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.type = data['type']
        self.edge_type = data["edge_type"]
        self.data['content']['edge_details'] = data['content']
        min_string = data['content']["min"]["Hours"] + ":" + data['content']["min"]["Minutes"] + ":" + \
                     data['content']["min"]["Seconds"]
        max_string = data['content']["max"]["Hours"] + ":" + data['content']["max"]["Minutes"] + ":" + \
                     data['content']["max"]["Seconds"]
        self.update_label(data['content']["title"], min_string, max_string)
        self.doSelect()  # reload the data when opening a new file
