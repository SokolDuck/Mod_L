from src.LR1.random_lemera import LemerRandomGenerator
from src.LR2.constants import COUNT, B, A, HIST_SIZE
import matplotlib.pyplot as plt
import numpy as np


class Generator:
    DISTRIBUTION_NAME: str
    have_ideal_example: bool = False

    def __init__(self, a=A, b=B, random_generator: LemerRandomGenerator = None, **kwargs):
        self.a = float(a)
        self.b = float(b)
        self.random_generator = random_generator

    def mean(self):
        return np.mean([self.next_random() for _ in range(COUNT)])

    def var(self):
        return np.var([self.next_random() for _ in range(COUNT)])

    def next_random(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def params(self):
        return r'a = {}, b = {}'.format(self.a, self.b)

    def ideal_example(self, *args, **kwargs):
        raise NotImplementedError


def generate_random_sequence(generator_obj, sequence_size=COUNT, *args, **kwargs):
    return [generator_obj.next_random(*args, **kwargs) for _ in range(sequence_size)]


def build_histogram(sequence: list, hist_size: int = HIST_SIZE, distribution_gen: Generator = None, _plt=plt, **kwargs):
    """
    :param sequence: list
    :param hist_size: int
    :param distribution_gen: Generator
    :param _plt: plot
    :param kwargs:
        - show_title: bool = True
        - pyqt5: boot = False
        - show: bool = True
    :return:
    """
    n, bins, patches = _plt.hist(sequence, hist_size, alpha=0.75, density=True)

    if distribution_gen:
        if kwargs.get('show_title', True):
            if kwargs.get('pyqt5', False):
                _plt.set_title(f'{distribution_gen.DISTRIBUTION_NAME} {distribution_gen.params}')
            else:
                _plt.title(f'{distribution_gen.DISTRIBUTION_NAME} {distribution_gen.params}')

        if distribution_gen.have_ideal_example:
            x, y = distribution_gen.ideal_example(sequence, **kwargs)
            _plt.plot(x, y, '-r')
        # else:
        #     _plt.plot(bins[:-1], [patch._y1 for patch in patches], '-r')

    if kwargs.get('show', True):
        _plt.show()


def print_sequence_on_plt(seq, distribution_gen: Generator = None, **kwargs):
    if distribution_gen:
        plt.title(f'{distribution_gen.DISTRIBUTION_NAME} {distribution_gen.params}')
    plt.plot(range(len(seq)), seq, 'bo')
    plt.show()


def get_mean_and_var(generator_obj: Generator, seq: list = None, **kwargs):
    print('-' * 32)
    print(f'{generator_obj.DISTRIBUTION_NAME}')

    print(f'Mean = {generator_obj.mean()}')

    if seq:
        print(f'check mean = {np.mean(seq)}')

    print(f'Var = {generator_obj.var()}')

    if seq:
        print(f'check var = {np.var(seq)}\n')


LAMER_RANDOM_GENERATOR = None


def run(distribution_class, **kwargs):
    """
    :param distribution_class: Generator
    :param kwargs:
        base_params
        - hist_size: int
        - sequence_size: int
        params_for_uniform
        - a: float
        - b: float
        params_for_gaussian
        - mu: float - mat ojidanie
        - sigma: float - sko
        - n: int
        params_for_triangular
        - left_right_triangular: str = l, r
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
    :return: None
    """
    global LAMER_RANDOM_GENERATOR

    if not LAMER_RANDOM_GENERATOR:
        LAMER_RANDOM_GENERATOR = LemerRandomGenerator()

    random_generator_obj = LAMER_RANDOM_GENERATOR
    generator_obj = distribution_class(random_generator=random_generator_obj, **kwargs)
    seq = generate_random_sequence(generator_obj, **kwargs)

    build_histogram(seq, distribution_gen=generator_obj, **kwargs)
    # print_sequence_on_plt(seq, distribution_gen=generator_obj)
    get_mean_and_var(generator_obj, seq)
