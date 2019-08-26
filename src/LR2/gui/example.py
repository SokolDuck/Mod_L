import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import importlib

from src.LR1.random_lemera import LemerRandomGenerator
from src.LR2.utils import generate_random_sequence, build_histogram
from src.LR2.constants import A, B, LAMBDA, ITA, MU, SIGMA, N

distribution_list = [
    'uniform',
    'exponential',
    'gamma',
    'gaussian',
    'simpson',
    'triangular',
]

params = [
    'param_1_label',
    'param_1',
    'param_2_label',
    'param_2',
    'param_3_label',
    'param_3',
]

distribution_params = {
    'uniform': {
        'param_1_label': 'A',
        'param_1': A,
        'param_2_label': 'B',
        'param_2': B,
    },
    'exponential': {
            'param_1_label': 'lambda',
            'param_1': LAMBDA,
    },
    'gamma': {
            'param_1_label': 'lambda',
            'param_1': LAMBDA,
            'param_2_label': 'ita',
            'param_2': ITA,
    },
    'gaussian': {
            'param_1_label': 'mu',
            'param_1': MU,
            'param_2_label': 'sigma',
            'param_2': SIGMA,
            'param_3_label': 'n',
            'param_3': N,
    },
    'simpson': {
            'param_1_label': 'A',
            'param_1': A,
            'param_2_label': 'B',
            'param_2': B,
    },
    'triangular': {
            'param_1_label': 'left or right (l, r)',
            'param_1': 'l',
            'param_2_label': 'A',
            'param_2': A,
            'param_3_label': 'B',
            'param_3': B,
    },
}

"""
params_for_uniform
- a: float
- b: float
params_for_gaussian
- mu: float - mat ojidanie
- sigma: float - sko
- n: int
params_for_triangular
- left_right_triangular: bool
- a: float
- b: float
params_for_exponential
- l: float - lambda
params_for_gamma
- l: float - lambda (a)
- ita: int - ita (k)
params_for_simpson
- a: float
- b: float
"""


class App(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.hist = None
        self.plot = None
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.hist = PlotCanvas(self)
        # self.plot = PlotCanvas(self, width=4, height=4, self.hist)
        self.hist.move(0, 0)
        # self.plot.move(0, 100)

        # button = QPushButton('PyQt5 button', self)
        # button.setToolTip('This s an example button')
        # button.move(500, 0)
        # button.resize(140, 100)

        for attr in params:
            getattr(self, attr).setVisible(False)

        self.generate_btn.clicked.connect(self.button_handler)
        self.distribution.addItems(distribution_list)

        self.distribution.activated[str].connect(self.set_distribution_params)

        self.show()
        self.button_handler()

    def set_mean_var(self, mean, var):
        self.mean_l.setText(str(mean))
        self.var_l.setText(str(var))

    def set_distribution_params(self, distribution_name):
        for name, value in distribution_params[distribution_name].items():
            attr = getattr(self, name)
            attr.setVisible(True)
            attr.setText(str(value))

    def get_distribution_params(self, distribution_name):
        return {}

    def button_handler(self, *args, **kwargs):
        sequence_size = int(self.sequence_size.value())
        hist_size = int(self.hist_size.value())
        distribution_name = str(self.distribution.currentText())

        mean, var = self.hist.plot(
            distribution_name,
            sequence_size=sequence_size,
            hist_size=hist_size,
            **self.get_distribution_params(distribution_name)
        )

        self.set_mean_var(mean, var)


class PlotCanvas(FigureCanvas):
    LAMER_RANDOM_GENERATOR = None

    def __init__(self, parent=None, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.mean, self.var = 0, 0

    def plot(self, distribution_name: str, **kwargs):
        distribution_module = importlib.import_module(f'src.LR2.distribution.{distribution_name}_distribution')
        distribution_class = getattr(distribution_module, f'{distribution_name.title()}Distribution')

        if not self.LAMER_RANDOM_GENERATOR:
            self.LAMER_RANDOM_GENERATOR = LemerRandomGenerator(**kwargs)

        distribution_gen = distribution_class(random_generator=self.LAMER_RANDOM_GENERATOR, **kwargs)
        data = generate_random_sequence(distribution_gen, **kwargs)

        self.axes.clear()

        hist_size = kwargs.get('hist_size')
        build_histogram(
            sequence=data,
            hist_size=hist_size,
            _plt=self.axes,
            show=False,
            distribution_gen=distribution_gen,
            pyqt5=True,
            show_title=False
        )

        # ax.hist(data, hist_size, alpha=0.75, density=True)
        # ax.set_title(f'{distribution_gen.DISTRIBUTION_NAME} {distribution_gen.params}')
        #
        # if distribution_gen.have_ideal_example:
        #     x, y = distribution_gen.ideal_example(data)
        #     ax.plot(x, y, '-r')

        self.draw()

        return distribution_gen.mean(), distribution_gen.var()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
