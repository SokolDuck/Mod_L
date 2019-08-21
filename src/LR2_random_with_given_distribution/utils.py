from src.LR2_random_with_given_distribution.constants import COUNT, B, A, X0, HIST_SIZE
import matplotlib.pyplot as plt
import numpy as np


class Generator:
    def __init__(self, a=A, b=B, random_generator=None):
        self.a = a
        self.b = b
        self.random_generator = random_generator

    def mean(self):
        raise NotImplementedError

    def var(self):
        raise NotImplementedError

    def next_random(self):
        raise NotImplementedError


def generate_random_sequence(generator_obj, sequence_size=COUNT):
    return [generator_obj.next_random() for _ in range(sequence_size)]


def build_histogram(sequence: list, hist_size: int = HIST_SIZE):
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
