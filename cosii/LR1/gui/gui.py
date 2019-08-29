import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from cosii.LR1.constants import FILE_PATH
from cosii.LR1.utils import get_img, ImageGenerator
from src.LR2.utils import generate_random_sequence, build_histogram, build_plot



class App(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example'
        self.width = 640
        self.height = 400
        self.hist = None
        self.plot = None
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle(self.title)

        self.original = PlotCanvas(self, image=True)
        self.hist = PlotCanvas(self, image=True)
        self.original.move(10, 0)
        self.hist.move(410, 0)

        self.a_slider.valueChanged.connect(self.slider_handler)
        self.b_slider.valueChanged.connect(self.slider_handler)

        self.show()

    def slider_handler(self):
        a_value = self.a_slider.value() / 10
        b_value = self.b_slider.value()
        self.a_value.setText(str(a_value))
        self.b_value.setText(str(b_value))
        self.hist.plot(a=a_value, b=b_value)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=4, dpi=100, hist=False, image=False):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.img_obj = ImageGenerator(file_path=FILE_PATH)

        if image:
            self.axes.imshow(self.img_obj.get_img(), cmap='gray')
        elif hist:
            build_histogram(self.img_obj.get_img_as_array(), 255, _plt=self.axes, show=False)

    def plot(self, a=0, b=0):
        array = self.img_obj.linear_correction(a=a, b=b)
        self.axes.clear()
        a_ = self.img_obj.get_img_from_array(array=array)

        self.axes.imshow(a_, cmap='gray')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
