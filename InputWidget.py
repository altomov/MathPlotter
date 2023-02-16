import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, QtCore


class InputWidget(QtWidgets.QWidget):
    commandEntered = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.input_text = QtWidgets.QPlainTextEdit(self)
        self.input_text.setPlainText("Enter commands here")
        self.input_text.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.input_text.setFixedHeight(80)
        
        
        self.run_button = QtWidgets.QPushButton("Run", self)
        self.run_button.clicked.connect(self.process_input)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.run_button)
        self.layout.setAlignment(QtCore.Qt.AlignBottom)

        # Connect the "Enter" key press event to the process_input method
        self.input_text.installEventFilter(self)

    def process_input(self):
        input_string = self.input_text.toPlainText()
        self.commandEntered.emit(input_string)

    def eventFilter(self, obj, event):
        # Handle key press events for the input box
        if obj == self.input_text and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return and event.modifiers() == QtCore.Qt.ControlModifier:
                self.process_input()
                return True
        return super().eventFilter(obj, event)