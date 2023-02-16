import matplotlib

from MatplotlibWidget import MatplotlibWidget
from InputWidget import InputWidget

matplotlib.use("Qt5Agg")
from PyQt5 import QtWidgets
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.matplotlib_widget = MatplotlibWidget(self)

        self.input_widget = InputWidget(self)
        self.input_widget.commandEntered.connect(self.handle_input)
        self.input_widget.setStyleSheet("")

        central_widget = QtWidgets.QWidget()
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 10)
        vlayout.addWidget(self.matplotlib_widget)
        vlayout.addWidget(self.input_widget)
        vlayout.setStretch(0, 10)
        vlayout.setStretch(1, 1)
        central_widget.setLayout(vlayout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("Math Plotter")
        self.showMaximized()

        self.add_point_action = QtWidgets.QAction("Add Point", self)
        self.add_point_action.triggered.connect(self.add_point)
        self.toolbar = self.addToolBar("Add Point")
        self.toolbar.addAction(self.add_point_action)

    def add_point(self):
        x, y = np.random.rand(2)
        self.matplotlib_widget.canvas.axes.scatter(x, y)
        self.matplotlib_widget.canvas.draw()

    def handle_input(self, input_string):
        print(input_string)
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()