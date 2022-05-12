import pytest
from unittest.mock import patch
from workflow_conf_nodes import WorkflowNode_Decision
from workflow_scene import WorkflowScene
from data_examples import editor_data_examples


@pytest.fixture
def scene_with_one_node_serialization(empty_scene):
    _ = WorkflowNode_Decision(scene=empty_scene)
    return empty_scene


@pytest.fixture
def empty_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    return scene

def equals_keys(dictionary1,dictionary2):
    for key in dictionary1:
        assert key in dictionary2
    for key in dictionary2:
        assert key in dictionary1

def all_values_with_same_type(dictionary1,dictionary2):
    for key in dictionary1:
        if key in dictionary2:
            assert type(dictionary1[key]) == type(dictionary2[key])

def test_empty_scene_serialization(empty_scene):
    equals_keys(empty_scene.serialize(), editor_data_examples["scene"]["editor empty scene"])
    all_values_with_same_type(empty_scene.serialize(), editor_data_examples["scene"]["editor empty scene"])

def test_node_in_scene(scene_with_one_node_serialization):
    equals_keys(scene_with_one_node_serialization.serialize()["nodes"][0], editor_data_examples["node"]["empty decision node"])
    all_values_with_same_type(scene_with_one_node_serialization.serialize()["nodes"][0], editor_data_examples["node"]["empty decision node"])

