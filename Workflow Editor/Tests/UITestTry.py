import pytest
from PyQt5 import QtCore
import workflow_window

@pytest.fixture
def app(qtbot):
    test_try = workflow_window.WorkflowEditorWindow()
    qtbot.addWidget(test_try)

    return test_try

def test_attributes_title(app):
    assert app.attributes.windowTitle() == "Attributes"

def test_nodes_title(app):
    assert app.items.windowTitle() == "Nodes"

def test_nodes_items(app):
    pass