import numpy as np
import math

from src.LR2_random_with_given_distribution.constants import LAMBDA, ITA
from src.LR2_random_with_given_distribution.utils import Generator, run


class GammaDistribution(Generator):
    DISTRIBUTION_NAME = 'Gamma distribution'
    have_ideal_example = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._lambda = kwargs.get('l', LAMBDA)
        self.ita = kwargs.get('ita', ITA)

    def next_random(self, *args, **kwargs):
        # return -1 / self._lambda * np.log(reduce(lambda x, y: x * y,
        #                                          [self.random_generator.get_next_random() for _ in range(self.ita)]))
        return (-1 / self._lambda) * sum([np.log(self.random_generator.get_next_random()) for _ in range(self.ita)])

    def ideal_example(self, sequence, *args, **kwargs):
        _max = max(sequence)
        x = [self.random_generator.get_next_random() * _max for _ in range(len(sequence))]
        x = sorted(x)
        con = (self._lambda ** self.ita) / math.factorial(self.ita - 1)

        return x, [con * (i ** (self.ita - 1)) * np.e ** (-i * self.ita) for i in x]

    def mean(self):
        return self.ita / self._lambda

    def var(self):
        return self.ita / self._lambda ** 2

    @property
    def params(self):
        return f'lambda = {self._lambda}, ita = {self.ita}'


if __name__ == '__main__':
    run(GammaDistribution, l=1, ita=2)
    run(GammaDistribution, l=1, ita=3)
    run(GammaDistribution, l=1, ita=4)
