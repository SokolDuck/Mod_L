import numpy as np

from src.LR2.constants import LAMBDA
from src.LR2.utils import Generator, run


class ExponentialDistribution(Generator):
    DISTRIBUTION_NAME = 'Exponential distribution'
    have_ideal_example = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lambda = kwargs.get('l', LAMBDA)

    def next_random(self, *args, **kwargs):
        return -1 / self._lambda * np.log(self.random_generator.get_next_random())

    def mean(self):
        return 1 / self._lambda

    def var(self):
        return 1 / (self._lambda ** 2)

    @property
    def params(self):
        return f'lambda = {self._lambda}'

    def ideal_example(self, sequence, *args, **kwargs):
        x = sorted(sequence)
        return x, [ self._lambda * np.exp(-i * self._lambda) for i in x]


if __name__ == '__main__':
    run(ExponentialDistribution, l=0.5)
    run(ExponentialDistribution, l=1)
    run(ExponentialDistribution, l=1.5)
