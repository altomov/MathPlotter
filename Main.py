import matplotlib

from MatplotlibWidget import MatplotlibWidget
from InputWidget import InputWidget

matplotlib.use("Qt5Agg")
from PyQt5 import QtWidgets
from Point import Point1
from Line import Line

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

        #Seperate in function - todo
        self.input_widget.point_created.connect(self.process_point)
        self.input_widget.line_created.connect(self.process_line)

    def process_point(self, point:Point1):
        self.matplotlib_widget.plot_points(point)   
    
    def process_line(self, line:Line):
        m = (line.end_point.y - line.start_point.y) / (line.end_point.x - line.start_point.x)
        c = line.start_point.y - m * line.start_point.x
        print("y=",m, "x+",c)
        self.matplotlib_widget.plot_line(line)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()