import numpy as np
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use("Qt5Agg")


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        super().__init__(parent)
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.canvas = FigureCanvas(fig)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        self.axes.set_aspect("equal")

        # Set the minimum and maximum x and y axis values
        self.axes.set_xlim([-8, 8])
        self.axes.set_ylim([-5, 5])

        self.axes.axhline(0, color='black', lw=2)
        self.axes.axvline(0, color='black', lw=2)

        self.axes.grid(visible=True, which='major',
                       color='black', linestyle='-')
        self.axes.minorticks_on()
        self.axes.grid(visible=True, which='minor',
                       color='green', linestyle='-', alpha=0.2)

        FigureCanvas.setSizePolicy(self.canvas,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self.canvas)

        # Store the starting coordinates for the move functionality
        self.x_start = None
        self.y_start = None

        # Connect the mouse events to the canvas
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)

    # Add the point to the plot
    def plot_points(self, point):
        color = [random.random() for i in range(3)]
        self.axes.scatter(point.x, point.y, color=color)
        self.axes.text(point.x + 0.05, point.y + 0.05, point.name)
        self.axes.figure.canvas.draw()
        print("Drawing")

    def clear_points(self):
        for coll in self.axes.collections:
            coll.remove()
            self.axes.figure.canvas.draw()

    def plot_line(self, line):
        x = np.linspace(-100, 100, 100)
        m = (line.end_point.y - line.start_point.y) / \
            (line.end_point.x - line.start_point.x)
        c = line.start_point.y - m * line.start_point.x
        y = m*x + c
        color = [random.random() for i in range(3)]
        self.axes.plot(x, y, color=color)
        self.axes.figure.canvas.draw()

    def plot_function(self, str):
        x = np.linspace(-100, 100, 5000)
        y = eval(str)
        color = [random.random() for i in range(3)]
        self.axes.plot(x, y, color = color)
        self.axes.figure.canvas.draw()

    def on_press(self, event):
        if event.button == 1:
            self.x_start = event.xdata
            self.y_start = event.ydata

    def on_release(self, event):
        if event.button == 1:
            x_offset = event.xdata - self.x_start
            y_offset = event.ydata - self.y_start
            self.axes.set_xlim(self.axes.get_xlim() - x_offset)
            self.axes.set_ylim(self.axes.get_ylim() - y_offset)
            self.canvas.draw()

    def on_scroll(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            scale_factor = 1.5
            if event.button == 'down':
                scale_factor = 1/scale_factor
            self.axes.set_xlim([x - (x - self.axes.get_xlim()[0])/scale_factor,
                                x + (self.axes.get_xlim()[1] - x)/scale_factor])
            self.axes.set_ylim([y - (y - self.axes.get_ylim()[0])/scale_factor,
                                y + (self.axes.get_ylim()[1] - y)/scale_factor])
            self.canvas.draw()
