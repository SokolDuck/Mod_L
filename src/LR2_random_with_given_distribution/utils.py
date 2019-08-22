from src.LR1.random_lemera import LemerRandomGenerator
from src.LR2_random_with_given_distribution.constants import COUNT, B, A, HIST_SIZE
import matplotlib.pyplot as plt
import numpy as np


class Generator:
    def __init__(self, a=A, b=B, random_generator: LemerRandomGenerator = None, **kwargs):
        self.a = a
        self.b = b
        self.random_generator = random_generator

    def mean(self):
        return np.mean([self.next_random() for _ in range(COUNT)])

    def var(self):
        return np.var([self.next_random() for _ in range(COUNT)])

    def next_random(self, *args, **kwargs):
        raise NotImplementedError


def generate_random_sequence(generator_obj, sequence_size=COUNT, *args, **kwargs):
    return [generator_obj.next_random(*args, **kwargs) for _ in range(sequence_size)]


def build_histogram(sequence: list, hist_size: int = HIST_SIZE, **kwargs):
    plt.hist(sequence, hist_size)
    plt.show()


def print_sequence_on_plt(seq):
    plt.plot(range(len(seq)), seq, 'bo')
    plt.show()


def get_mean_and_var(generator_obj, seq: list = None):
    print(f'Mean = {generator_obj.mean()}')

    if seq:
        print(f'check mean = {np.mean(seq)}')

    print(f'Var = {generator_obj.var()}')

    if seq:
        print(f'check var = {np.var(seq)}')


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
        - m: float
        - sko: float
        - n: int
        params_for_triangular
        - left_right_triangular: bool
    :return: None
    """
    global LAMER_RANDOM_GENERATOR

    if not LAMER_RANDOM_GENERATOR:
        LAMER_RANDOM_GENERATOR = LemerRandomGenerator()

    random_generator_obj = LAMER_RANDOM_GENERATOR
    generator_obj = distribution_class(random_generator=random_generator_obj, **kwargs)
    seq = generate_random_sequence(generator_obj, **kwargs)

    build_histogram(seq, **kwargs)
    print_sequence_on_plt(seq)
    get_mean_and_var(generator_obj, seq)
