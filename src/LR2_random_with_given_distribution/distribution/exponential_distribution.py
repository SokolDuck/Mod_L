import numpy as np

from src.LR2_random_with_given_distribution.constants import LAMBDA
from src.LR2_random_with_given_distribution.utils import Generator, run


class ExponentialDistribution(Generator):
    DISTRIBUTION_NAME = 'Exponential distribution'

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


if __name__ == '__main__':
    run(ExponentialDistribution, l=0.5)
    run(ExponentialDistribution, l=1)
    run(ExponentialDistribution, l=1.5)
