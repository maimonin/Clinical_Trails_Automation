import pytest
from unittest.mock import patch

from Tests.Serialization.data_examples import editor_data_examples, node_classes, engine_data_examples
from Tests.Serialization.general_utils import equals_flows
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import *
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


@pytest.fixture
def new_decision_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_Decision(scene=scene)
        # node.callback_from_window()
    return node


@pytest.fixture
def modified_decision_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_Decision(scene=scene)
        new_content = {
            {"node_details": {"title": "New Decision Node"},
             "condition": [{
                 "title": "First",
                 "type": "trait condition",
                 "trait": "age",
                 "satisfy": {
                     "type": "range",
                     "value": {"min": 0, "max": 10}

                 }}, {
                 "title": "second",
                 "type": "test condition",
                 "test": "blood",
                 "satisfy": {
                     "type": "one_choice",
                     "value": "b+"

                 }
             }
                 , {
                     "title": "third",
                     "type": "questionnaire condition",
                     "questionnaireNumber": 1,
                     "questionNumber": 2,
                     "acceptedAnswers": [1, 2]
                 }

             ]}
        }
        node.callback_from_window(new_content)
    return node


@pytest.fixture
def new_notification_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        # with patch("workflow_node_base.WorkflowGraphicWithIcon"):
        #     with patch("QGraphicsTextItem.QGraphicsTextItem"):
        node = WorkflowNode_SimpleString(scene=scene)
    return node


@pytest.fixture
def modified_notification_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_SimpleString(scene=scene)
        new_content = {
            "Node Details": [{'name': 'changed title', 'type': 'text', 'value': 'New Notification Node'},
                             {'name': 'Actors', 'type': 'checklist',
                              'options': ['Nurse', 'Doctor', 'Participant', 'Investigator', 'Lab Technician'],
                              'value': ['Nurse']}, {'name': 'Color', 'type': 'combobox icons', 'value': 'Grey',
                                                    'options': ['Grey', 'Yellow', 'Orange', 'Red', 'Pink', 'Green',
                                                                'Blue']}],
            "Notification": [{'name': 'Text', 'type': 'text', 'value': 'changed notification value'}],
            "callback": None
        }
        node.callback_from_window(new_content)
    return node


@pytest.fixture
def new_complex():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_ComplexNode(scene=scene)
    return node


@pytest.fixture
def new_test_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_DataEntry(scene=scene)
    return node


@pytest.fixture
def new_questionnaire_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_Questionnaire(scene=scene)
    return node

@pytest.fixture
def modified_questionnaire_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_SimpleString(scene=scene)
        new_content = {
                    "node_details": {
                        "title": "changed title",
                    },
                    "questions": [],
                    "qusetionnaire_number": 1
                }
        node.callback_from_window(new_content)
    return node

@pytest.fixture
def new_start_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_Start(scene=scene)
    return node


@pytest.fixture
def new_finish_node():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        node = WorkflowNode_Finish(scene=scene)
    return node

def test_new_decision_serialization(new_decision_node):
    assert equals_flows(new_decision_node.serialize(engine_save=True),
                        engine_data_examples["scene"]["editor empty scene"])
    assert equals_nodes(new_decision_node.serialize(engine_save=True)["nodes"][0],
                        engine_data_examples["node"]["empty decision node"])


def test_modified_decision_serialization(modified_decision_node):
    assert equals_flows(modified_decision_node.serialize(engine_save=True),
                        engine_data_examples["node"]["decision"]["with all condition types"])


def test_empty_notification_serialization(new_notification_node):
    assert equals_flows(new_notification_node.serialize(engine_save=True),
                        engine_data_examples["node"]["simple string"]["empty"])


def test_modified_notification_serialization(modified_notification_node):
    assert equals_flows(modified_notification_node.serialize(engine_save=True),
                        engine_data_examples["node"]["simple string"]["with_changes"])


def test_empty_complex_serialization(new_complex):
    assert equals_flows(new_complex.serialize(engine_save=True),
                        engine_data_examples["node"]["complex"]["empty"])


def test_empty_test_serialization(new_test_node):
    assert equals_flows(new_test_node.serialize(engine_save=True),
                        engine_data_examples["node"]["test"]["empty"])


def test_empty_questionnaire_serialization(new_questionnaire_node):
    assert equals_flows(new_questionnaire_node.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["empty"])


def test_modified_questionnaire_serialization(modified_questionnaire_node):
    assert equals_flows(modified_questionnaire_node.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["changed title"])


def test_empty_start_serialization(new_start_node):
    assert equals_flows(new_start_node.serialize(engine_save=True),
                        engine_data_examples["node"]["start"]["empty"])


def test_empty_finish_serialization(new_finish_node):
    assert equals_flows(new_finish_node.serialize(engine_save=True),
                        engine_data_examples["node"]["finish"]["empty"])


def test_empty_decision_node(empty_decision_node):
    assert equals_nodes(empty_decision_node.serialize(engine_save=True),
                        engine_data_examples["node"]["empty decision node"])


def test_general_engine_node_structure(all_node_types_instances):
    for node in all_node_types_instances:
        serialized = node.serialize()
        for key in engine_data_examples["node"]["node general structure"]:
            assert key in serialized and \
                   type(serialized[key]) == engine_data_examples["node"]["node general structure"][key]
