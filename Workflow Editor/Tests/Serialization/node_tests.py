import pytest
from unittest.mock import patch

from Tests.Serialization.data_examples import editor_data_examples, node_classes, engine_data_examples
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import WorkflowNode_Decision
from workflow_scene import WorkflowScene


@pytest.fixture
def empty_decision_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_Decision(scene=scene)
    return node


@pytest.fixture
def all_node_types_instances():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    with patch("workflow_node_base.WorkflowGraphicSmallDiamond.initUI"):
        with patch("workflow_node_base.grScene.initUI"):
            nodes = [node_type(scene=scene) for node_type in node_classes]
    return nodes



def test_empty_decision_node(empty_decision_node):
    assert equals_nodes(empty_decision_node.serialize(),
                        editor_data_examples["node"]["empty decision node"])


def test_general_engine_node_structure(all_node_types_instances):
    for node in all_node_types_instances:
        serialized = node.serialize()
        for key in engine_data_examples["node"]["node general structure"]:
            assert key in serialized and \
                   type(serialized[key]) == engine_data_examples["node"]["node general structure"][key]
