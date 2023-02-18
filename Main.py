from Line import Line
from Point import Point1
from PyQt5.QtWidgets import QAction, QToolBar, QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout
from PyQt5 import QtWidgets
import matplotlib

from MatplotlibWidget import MatplotlibWidget
from InputWidget import InputWidget
from NewPointDialog import AddPointDialog
from MakeLineDialog import AddLineDialog

matplotlib.use("Qt5Agg")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.matplotlib_widget = MatplotlibWidget(self)

        self.input_widget = InputWidget(self)

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

        self.create_actions()
        self.create_toolbars()
        self.connect_actions()

        # Seperate in function - todo
        self.input_widget.point_created.connect(self.process_point)
        self.input_widget.line_created.connect(self.process_line)

    def create_actions(self):
        self.create_point_action = QAction("&Add point", self)
        self.create_line_action = QAction("&Add line", self)

        self.clear_board = QAction("&Clear board", self)

    def create_toolbars(self):
        basic_toolbar = QToolBar("Basic", self)
        basic_toolbar.setFixedHeight(72)
        self.addToolBar(basic_toolbar)
        basic_toolbar.addAction(self.create_point_action)
        basic_toolbar.addAction(self.create_line_action)

        miscellaneous_toolbar = QToolBar("Miscellaneous", self)
        self.addToolBar(miscellaneous_toolbar)
        miscellaneous_toolbar.addAction(self.clear_board)

    def connect_actions(self):
        self.create_point_action.triggered.connect(self.add_point)
        self.create_line_action.triggered.connect(self.add_line)

        # self.clear_board.triggered.connect(self.clear_all_objects)

    # Add point from toolbar button
    def add_point(self):
        dialog = AddPointDialog(self)
        if dialog.exec_():
            x, y, name = dialog.get_values()
            input = f'{name}({x};{y})'
            self.input_widget.process_input(input, source='button')
            print(f"Added point: {name}({x}, {y})")
            print(self.input_widget.points)

    # Add line from toolbar button
    def add_line(self):
        line_dialog = AddLineDialog(self)
        if line_dialog.exec_() == QDialog.Accepted:
            start_point, end_point = line_dialog.get_values()
            input = f'{"Line"}({start_point},{end_point})'
            self.input_widget.process_input(input, source='button')
            print(start_point, end_point)

    def process_point(self, point: Point1):
        self.matplotlib_widget.plot_points(point)

    def process_line(self, line: Line):
        m = (line.end_point.y - line.start_point.y) / \
            (line.end_point.x - line.start_point.x)
        c = line.start_point.y - m * line.start_point.x
        print("y=", m, "x+", c)
        self.matplotlib_widget.plot_line(line)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
