import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from cosii.LR1.constants import FILE_PATH
from cosii.LR1.image_corrector import ImageCorrector
from src.LR2.utils import build_histogram


class App(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example'
        self.width = 640
        self.height = 400
        self.hist = None
        self.original = None
        self.plot = None
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle(self.title)

        self.original = PlotCanvas(self, image=True)
        self.hist = PlotCanvas(self, image=True)
        self.original.move(10, 0)
        self.hist.move(810, 0)

        self.a_slider.valueChanged.connect(self.linear_handler)
        self.b_slider.valueChanged.connect(self.linear_handler)

        self.A_slider.valueChanged.connect(self.gamma_handler)
        self.y_slider.valueChanged.connect(self.gamma_handler)

        self.log_a.valueChanged.connect(self.logarithmic_correction)

        self.btn.clicked.connect(self.build_hist)

        self.show()
        self.linear_handler()

    def logarithmic_correction(self):
        value = self.log_a.value() / 100
        self.log_a_label.setText(str(value))
        self.hist.plot_log(value)

    def linear_handler(self):
        a_value = self.a_slider.value()
        b_value = self.b_slider.value()
        self.a_value.setText(str(a_value))
        self.b_value.setText(str(b_value))
        self.hist.plot_linear(a=a_value, b=b_value)

    def gamma_handler(self):
        a = self.A_slider.value() / 10
        y = self.y_slider.value() / 10
        self.A_value.setText(str(a))
        self.y_value.setText(str(y))
        self.hist.plot_gamma(A=a, y=y)

    def build_hist(self):
        self.original.build_hist()
        self.hist.build_hist()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=4, dpi=200, hist=False, image=False):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.img_obj = ImageCorrector(file_path=FILE_PATH)
        self.img = self.img_obj.get_img()

        if image:
            self.axes.imshow(self.img_obj.get_img(), cmap='gray')
            # plt.imshow(self.img_obj.get_img(), cmap='gray')
            # plt.show()
        elif hist:
            build_histogram(self.img_obj.get_img_as_array(), 255, _plt=self.axes, show=False)

    def plot_linear(self, a=0, b=0):
        array = self.img_obj.linear_correction(a, b)
        self.plot(array)

    def plot_gamma(self, A, y):
        array = self.img_obj.gamma_correction(A, y)
        self.plot(array)

    def plot_log(self, c):
        array = self.img_obj.logarithmic_correction(c)
        self.plot(array)

    def plot(self, array):
        self.axes.clear()
        self.img = self.img_obj.get_img_from_array(array=array)
        self.axes.imshow(self.img)
        self.draw()

    def build_hist(self):
        plt.hist(self.img.ravel(), 255, density=True)
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
