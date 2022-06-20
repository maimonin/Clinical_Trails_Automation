import pytest
from unittest.mock import patch

from Tests.Serialization.data_examples import engine_data_examples
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import WorkflowNode_Questionnaire
from workflow_scene import WorkflowScene



@pytest.fixture
def questionnaire_node_with_changed_title():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_Questionnaire(scene=scene)
    node.callback_from_window({
        'Node Details': [{
            'name': 'Title',
            'type': 'text',
            'value': 'changed title'
        }, {
            'name': 'Color',
            'type': 'combobox icons',
            'value': 'Grey',
            'options': ['Grey', 'Yellow', 'Orange', 'Red', 'Pink', 'Green', 'Blue']
        }
        ],
        'Content': [{
            'name': 'Questionnaire #',
            'type': 'text',
            'value': '1'
        }, {
            'name': 'Questions',
            'type': 'q sub tree',
            'value': []
        }
        ],
        'callback': None
    }
    )
    return node


def test_questionnaire_node_with_changed_title_serialization(questionnaire_node_with_changed_title):
    assert equals_nodes(questionnaire_node_with_changed_title.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["changed title"])


@pytest.fixture
def questionnaire_node_with_changed_questionnaire_number():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_Questionnaire(scene=scene)
    node.callback_from_window({
        'Node Details': [{
            'name': 'Title',
            'type': 'text',
            'value': 'changed title'
        }, {
            'name': 'Color',
            'type': 'combobox icons',
            'value': 'Grey',
            'options': ['Grey', 'Yellow', 'Orange', 'Red', 'Pink', 'Green', 'Blue']
        }
        ],
        'Content': [{
            'name': 'Questionnaire #',
            'type': 'text',
            'value': '1'
        }, {
            'name': 'Questions',
            'type': 'q sub tree',
            'value': []
        }
        ],
        'callback': None
    }
    )
    return node


def test_questionnaire_node_with_changed_questionnaire_number_serialization(
        questionnaire_node_with_changed_questionnaire_number):
    assert equals_nodes(questionnaire_node_with_changed_questionnaire_number.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["changed questionnaire number"])

@pytest.fixture
def questionnaire_node_with_one_multiple_choice_question():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_Questionnaire(scene=scene)
    node.callback_from_window({
        'Node Details': [{
            'name': 'Title',
            'type': 'text',
            'value': 'changed title'
        }, {
            'name': 'Color',
            'type': 'combobox icons',
            'value': 'Grey',
            'options': ['Grey', 'Yellow', 'Orange', 'Red', 'Pink', 'Green', 'Blue']
        }
        ],
        'Content': [{
            'name': 'Questionnaire #',
            'type': 'text',
            'value': '1'
        }, {
            'name': 'Questions',
            'type': 'q sub tree',
            'value': [{
                    'id': 1,
                    'type': 'multi',
                    'text': 'multiple question',
                    'options': ['option 1',"option 2", None, None, None, None]
                }]
        }
        ],
        'callback': None
    }
    )
    return node


def test_questionnaire_node_with_one_multiple_question_serialization(
        questionnaire_node_with_one_multiple_choice_question):
    assert equals_nodes(questionnaire_node_with_one_multiple_choice_question.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["one multi question"])

@pytest.fixture
def questionnaire_node_with_one_single_choice_question():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_Questionnaire(scene=scene)
    node.callback_from_window({
        'Node Details': [{
            'name': 'Title',
            'type': 'text',
            'value': 'changed title'
        }, {
            'name': 'Color',
            'type': 'combobox icons',
            'value': 'Grey',
            'options': ['Grey', 'Yellow', 'Orange', 'Red', 'Pink', 'Green', 'Blue']
        }
        ],
        'Content': [{
            'name': 'Questionnaire #',
            'type': 'text',
            'value': '1'
        }, {
            'name': 'Questions',
            'type': 'q sub tree',
            'value': [{
                    'id': 1,
                    'type': 'one choice',
                    'text': 'single choice question',
                    'options': ['option 1',"option 2", None, None, None, None]
                }]
        }
        ],
        'callback': None
    }
    )
    return node


def test_questionnaire_node_with_one_single_choice_question_serialization(
        questionnaire_node_with_one_single_choice_question):
    assert equals_nodes(questionnaire_node_with_one_single_choice_question.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["one single choice question"])

@pytest.fixture
def questionnaire_node_with_one_open_question():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    node = WorkflowNode_Questionnaire(scene=scene)
    node.callback_from_window({
        'Node Details': [{
            'name': 'Title',
            'type': 'text',
            'value': 'changed title'
        }, {
            'name': 'Color',
            'type': 'combobox icons',
            'value': 'Grey',
            'options': ['Grey', 'Yellow', 'Orange', 'Red', 'Pink', 'Green', 'Blue']
        }
        ],
        'Content': [{
            'name': 'Questionnaire #',
            'type': 'text',
            'value': '1'
        }, {
            'name': 'Questions',
            'type': 'q sub tree',
            'value': [{
                    'id': 1,
                    'type': 'multi',
                    'text': 'open question',
                }]
        }
        ],
        'callback': None
    }
    )
    return node


def test_questionnaire_node_with_one_open_question_serialization(
        questionnaire_node_with_one_open_question):
    assert equals_nodes(questionnaire_node_with_one_open_question.serialize(engine_save=True),
                        engine_data_examples["node"]["questionnaire"]["one open question"])
