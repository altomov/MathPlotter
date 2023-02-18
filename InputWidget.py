import re
from Line import Line
from Point import Point1
from PyQt5 import QtWidgets, QtCore, QtGui
import matplotlib
matplotlib.use("Qt5Agg")

POINT_REGEX = r"([A-Za-z]+)\(([\d,.]+);([\d,.]+)\)"
LINE_REGEX = r'^Line\(([A-Za-z]),\s*([A-Za-z])\)$'
FUNCTION_REGEX = r'[a-zA-Z]+\([a-zA-Z]\)'


class InputWidget(QtWidgets.QWidget):
    point_created = QtCore.pyqtSignal(Point1)
    line_created = QtCore.pyqtSignal(Line)
    function_created = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = {}

        self.input_text = QtWidgets.QPlainTextEdit(self)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.input_text.setFont(font)

        self.input_text.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.input_text.setFixedHeight(80)

        self.run_button = QtWidgets.QPushButton("Run", self)
        self.run_button.clicked.connect(self.process_input)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.run_button)
        self.layout.setAlignment(QtCore.Qt.AlignBottom)

        self.input_text.installEventFilter(self)

    def process_input(self, input_string=None, source='widget'):

        if source == 'widget':
            input_string = self.input_text.toPlainText()

        match_point = re.match(POINT_REGEX, input_string, re.IGNORECASE)
        match_line = re.match(LINE_REGEX, input_string, re.IGNORECASE)
        macth_function = re.match(FUNCTION_REGEX, input_string, re.IGNORECASE)

        if match_point:
            try:
                name, x_str, y_str = match_point.groups()
                x = float(x_str)
                y = float(y_str)

                if name in self.points:
                    print("Point with the same name already exists!")
                    return
                for p in self.points.values():
                    if p.x == x and p.y == y:
                        print("Point with the same coordinates already exists!")
                        return

                point = Point1(name, x, y)
                self.points[name] = point
                self.point_created.emit(point)

                self.clear_input()

            except ValueError:
                print("Value error")
        elif match_line:
            try:
                point1_name = match_line.group(1)
                point2_name = match_line.group(2)

                if point1_name == point2_name:
                    print("You have entered two identical points!")

                if point1_name not in self.points:
                    print(f"Point '{point1_name}' does not exist!")
                    return

                if point2_name not in self.points:
                    print(f"Point '{point2_name}' does not exist!")
                    return

                point1 = self.points[point1_name]
                point2 = self.points[point2_name]

                line = Line(point1, point2)
                self.line_created.emit(line)

                self.clear_input()

            except ValueError:
                print("Value error")

        elif 'x' in input_string:
            pattern = r'(\d+)([a-zA-Z])'
            replace = r'\1*\2'

            result = re.sub(pattern, replace, input_string)

            self.function_created.emit(result)
            self.clear_input()
            
        else:
            print("Invalid input")


    def eventFilter(self, obj, event):
        if obj == self.input_text and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                self.process_input()
                return True
        return super().eventFilter(obj, event)

    def clear_input(self):
        self.input_text.setPlainText("")
