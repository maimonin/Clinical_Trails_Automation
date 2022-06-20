import pytest
from unittest.mock import patch

from Tests.Serialization.data_examples import editor_data_examples, node_classes, engine_data_examples
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import *
from workflow_scene import WorkflowScene


@pytest.fixture
def empty_decision_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_Decision(scene=scene)
    return node


def test_empty_decision_node(empty_decision_node):
    assert equals_nodes(empty_decision_node.serialize(engine_save=True),
                        engine_data_examples["node"]["decision"]["empty"])


@pytest.fixture
def empty_complex_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_ComplexNode(scene=scene)
    return node


def test_empty_complex_node(empty_complex_node):
    assert equals_nodes(empty_complex_node.serialize(engine_save=True),
                        engine_data_examples["node"]["complex"]["empty"])


@pytest.fixture
def empty_simple_string_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_SimpleString(scene=scene)
    return node


def test_empty_simple_string_node(empty_simple_string_node):
    assert equals_nodes(empty_simple_string_node.serialize(engine_save=True),
                        engine_data_examples["node"]["simple string"]["empty"])


@pytest.fixture
def empty_data_entry_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()

    node = WorkflowNode_DataEntry(scene=scene)
    return node


def test_empty_data_entry_node(empty_data_entry_node):
    assert equals_nodes(empty_data_entry_node.serialize(engine_save=True),
                        engine_data_examples["node"]["data entry"]["empty"])


@pytest.fixture
def empty_questionnaire_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()

    node = WorkflowNode_Questionnaire(scene=scene)
    return node


def test_empty_questionnaire_node(empty_questionnaire_node):
    assert equals_nodes(empty_questionnaire_node.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["empty"])

@pytest.fixture
def start_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()

    node = WorkflowNode_Start(scene=scene)
    return node

def test_start_node(start_node):
    assert equals_nodes(start_node.serialize(engine_save=True),
                        engine_data_examples["node"]["start"])


@pytest.fixture
def finish_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()

    node = WorkflowNode_Finish(scene=scene)
    return node

def test_finish_node(finish_node):
    assert equals_nodes(finish_node.serialize(engine_save=True),
                        engine_data_examples["node"]["finish"])
