import pytest
from unittest.mock import patch

from Tests.Serialization.general_utils import are_similar_, equals_flows
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import *
from workflow_scene import WorkflowScene
from data_examples import *


@pytest.fixture
def scene_with_decision_node_serialization():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_Decision(scene=scene)
        node.callback_from_window()
    return scene


@pytest.fixture
def empty_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    return scene


@pytest.fixture
def scene_empty_notification_serialization():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        with patch("workflow_node_base.WorkflowGraphicWithIcon"):
            node = WorkflowNode_SimpleString(scene=scene)
    return scene


def test_empty_scene_serialization(empty_scene):
    assert equals_flows(empty_scene.serialize(), editor_data_examples["scene"]["editor empty scene"])


def test_node_in_scene(scene_with_decision_node_serialization):
    assert equals_flows(scene_with_decision_node_serialization.serialize(),
                        editor_data_examples["scene"]["editor empty scene"])
    assert equals_nodes(scene_with_decision_node_serialization.serialize()["nodes"][0],
                        editor_data_examples["node"]["empty decision node"])


def test_empty_notification(scene_empty_notification_serialization):
    assert equals_flows(scene_empty_notification_serialization.serialize(),
                        engine_data_examples["node"]["simple string"]["empty"])
