import pytest
from unittest.mock import patch

from Tests.Serialization.data_examples import engine_data_examples
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import WorkflowNode_SimpleString
from workflow_scene import WorkflowScene


@pytest.fixture
def simple_string_node_with_changed_value():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_SimpleString(scene=scene)
    node.callback_from_window({'Node Details': [{'name': 'Title', 'type': 'text', 'value': 'changed title'},
                                                {'name': 'Actors', 'type': 'checklist',
                                                 'options': ['Nurse', 'Doctor', 'Participant', 'Investigator',
                                                             'Lab Technician'], 'value': ['Nurse']},
                                                {'name': 'Color', 'type': 'combobox icons', 'value': 'Grey',
                                                 'options': ['Grey', 'Yellow', 'Orange', 'Red', 'Pink', 'Green',
                                                             'Blue']}], 'Notification': [
        {'name': 'Text', 'type': 'text', 'value': 'changed notification value'}], 'callback': None})
    return node


def test_simple_string_node_changes(simple_string_node_with_changed_value):
    assert equals_nodes(simple_string_node_with_changed_value.serialize(engine_save=True),
                        engine_data_examples["node"]["simple string"]["with_changes"])
