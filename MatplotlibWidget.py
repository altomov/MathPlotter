import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
        self.axes.set_aspect("equal", 'box')
        #self.setMaximumSize(400,400)
        self.axes.axhline(0, color='black', lw=2)
        self.axes.axvline(0, color='black', lw=2)

        self.axes.grid(visible=True, which='major', color='black', linestyle='-')
        self.axes.minorticks_on()
        self.axes.grid(visible=True, which='minor', color='green', linestyle='-', alpha=0.2)


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        # store the starting coordinates for the move functionality
        self.x_start = None
        self.y_start = None
        
        
        # Connect the mouse events to the canvas
        self.mpl_connect('button_press_event', self.on_press)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('scroll_event', self.on_scroll)


    
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
            self.draw()

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
            self.draw()



class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = MplCanvas(self)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

