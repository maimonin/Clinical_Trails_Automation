from collections import OrderedDict
from nodeeditor.node_edge import Edge, EDGE_TYPE_DIRECT
from nodeeditor.utils import dumpException
from workflow_graphics_edge import WFGraphicsEdgeText, WFGraphicsRegularEdgeWithText
from PyQt5.QtCore import QTime

NORMAL = 0
RELATIVE = 1


class WorkflowEdge(Edge):

    def __init__(self, scene: 'Scene', start_socket: 'Socket' = None, end_socket: 'Socket' = None,
                 edge_type=EDGE_TYPE_DIRECT, text="No Title", attributes_dock_callback=None):
        self._text = text
        super().__init__(scene, start_socket, end_socket, edge_type)
        # data for engine
        self.data = {
            "content": {
                "edge_details": {
                    "title": "",
                    "min": {"hours": "00", "minutes": "00", "seconds": "00"},
                    "max": {"hours": "00", "minutes": "00", "seconds": "00"},
                },
                "callback": self.callback_from_dock,

            }}
        self.text = text
        self.type = NORMAL

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



    def getGraphicsEdgeClass(self):
        """Returns the class representing Graphics Edge"""
        return WFGraphicsRegularEdgeWithText

    def doSelect(self, new_state: bool = True):
        self.grEdge.text = self.text
        try:
            if new_state:
                self.get_dock_callback()(self.get_tree_build())
            else:
                self.scene.get_dock_callback()(None)
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
            # TODO: make sure min is smaller than max
            if input_min != "":
                self.data["content"]["edge_details"]["min"]["hours"] = input_min[:2]
                self.data["content"]["edge_details"]["min"]["minutes"] = input_min[3:5]
                self.data["content"]["edge_details"]["min"]["seconds"] = input_min[6:]
            if input_max != "":
                self.data["content"]["edge_details"]["max"]["hours"] = input_max[:2]
                self.data["content"]["edge_details"]["max"]["minutes"] = input_max[3:5]
                self.data["content"]["edge_details"]["max"]["seconds"] = input_max[6:]
        except Exception as e:
            dumpException(e)

    def update_label(self, input_title, input_min, input_max):
        if input_title == "":
            self.text = "No Title"
            if input_min != "" and input_min != "00:00:00" and input_max != "" and input_max != "00:00:00":
                self.text = input_min + " - " + input_max
        else:
            self.text = input_title
            if input_min != "" and input_min != "00:00:00" and input_max != "" and input_max != "00:00:00":
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
        dict_to_string = time_dict["hours"] + ":" + time_dict["minutes"] + ":" + time_dict["seconds"]
        result = QTime.fromString(dict_to_string, "hh:mm:ss")
        return result

    def get_dock_callback(self):
        return self.scene.getDockCallback()

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
            if self.type == RELATIVE:
                del result["content"]["title"]
                result["content"]["min"]["hours"] = int(result["content"]["min"]["hours"])
                result["content"]["min"]["seconds"] = int(result["content"]["min"]["seconds"])
                result["content"]["min"]["minutes"] = int(result["content"]["min"]["minutes"])

                result["content"]["max"]["hours"] = int(result["content"]["max"]["hours"])
                result["content"]["max"]["seconds"] = int(result["content"]["max"]["seconds"])
                result["content"]["max"]["minutes"] = int(result["content"]["max"]["minutes"])

        return result

    def deserialize(self, data: dict, hashmap: dict = {}, restore_id: bool = True, *args, **kwargs) -> bool:
        if restore_id: self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.type = data['type']
        self.edge_type = data["edge_type"]
        # FIXME: in case of NORMAL edge, there's no content key.
        self.data['content']['edge_details'] = data['content']
        min_string = data['content']["min"]["hours"] + ":" + data['content']["min"]["minutes"] + ":" + \
                     data['content']["min"]["seconds"]
        max_string = data['content']["max"]["hours"] + ":" + data['content']["max"]["minutes"] + ":" + \
                     data['content']["max"]["seconds"]
        self.update_label(data['content']["title"], min_string, max_string)
        self.doSelect()  # reload the data when opening a new file
