import pytest
from unittest.mock import patch

from Tests.Serialization.general_utils import are_similar_
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import WorkflowNode_Decision
from workflow_scene import WorkflowScene
from data_examples import editor_data_examples


@pytest.fixture
def scene_with_one_node_serialization():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        _ = WorkflowNode_Decision(scene=scene)
    return scene


@pytest.fixture
def empty_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    return scene


def test_empty_scene_serialization(empty_scene):
    assert are_similar_(empty_scene.serialize(), editor_data_examples["scene"]["editor empty scene"])

def test_node_in_scene(scene_with_one_node_serialization):
    assert are_similar_(scene_with_one_node_serialization.serialize(), editor_data_examples["scene"]["editor empty scene"])
    assert equals_nodes(scene_with_one_node_serialization.serialize()["nodes"][0],
                 editor_data_examples["node"]["empty decision node"])
