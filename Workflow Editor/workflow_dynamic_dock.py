from PyQt5.QtWidgets import QDockWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QComboBox


class QDynamicDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Attributes")
        # self.setWidget(QPushButton("Save",self))


    def setAsEdge(self):
        layout = QFormLayout()

        timeLabel = QLabel()
        timeLabel.setText("Time Constraint")

        timeInput = QLineEdit()
        timeInput.setPlaceholderText("0")

        layout.addRow(timeLabel, timeInput)
        self.setLayout(layout)

    def setNodeDetails(self):
        layout = QFormLayout()
        # Node details
        titleLabel = QLabel("Title")
        titleInput = QLineEdit()
        titleInput.setPlaceholderText("Questionnaire")
        layout.addRow(titleLabel, titleInput)

        timeLabel = QLabel("Time")
        timeInput = QLineEdit()
        timeInput.setPlaceholderText("0")
        layout.addRow(timeLabel, timeInput)

        inChargeLabel = QLabel("Actor In Charge")
        inChargeInput = QComboBox()
        inChargeInput.addItem("Nurse")
        inChargeInput.addItem("Doctor")
        inChargeInput.addItem("Investigator")
        inChargeInput.addItem("Participant")
        inChargeInput.addItem("Lab Technician")
        layout.addRow(inChargeLabel, inChargeLabel)

        # TODO: Add Actor

        return layout

    def setAsQuestionnaire(self):
        layout = self.setNodeDetails()
        self.setLayout(layout)