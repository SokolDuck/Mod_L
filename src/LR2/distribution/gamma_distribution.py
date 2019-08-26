import numpy as np
import math

from src.LR2.constants import LAMBDA, ITA
from src.LR2.utils import Generator, run


class GammaDistribution(Generator):
    DISTRIBUTION_NAME = 'Gamma distribution'
    have_ideal_example = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._lambda = float(kwargs.get('l', LAMBDA))
        self.ita = int(kwargs.get('ita', ITA))

    def next_random(self, *args, **kwargs):
        # return -1 / self._lambda * np.log(reduce(lambda x, y: x * y,
        #                                          [self.random_generator.get_next_random() for _ in range(self.ita)]))
        return (-1 / self._lambda) * sum([np.log(self.random_generator.get_next_random()) for _ in range(self.ita)])

    def ideal_example(self, sequence, *args, **kwargs):
        # distribution density
        #                                                 lambda ** ita
        #   ? x>0 = x ** (ita - 1) * e ** (-x * lambda) * --------------
        #                                                 (ita - 1) !

        #                               e ** (-x / lambda)
        #   ? x>0 = x ** (ita - 1) * ------------------------------
        #                               lambda ** ita * (ita - 1) !

        x = sorted(sequence)
        con = self._lambda ** self.ita / math.factorial(self.ita - 1)

        return x, [con * i ** (self.ita - 1) * np.e ** (-i * self._lambda) for i in x]

    def mean(self):
        return self.ita / self._lambda

    def var(self):
        return self.ita / self._lambda ** 2

    @property
    def params(self):
        return f'lambda = {self._lambda}, ita = {self.ita}'


if __name__ == '__main__':
    run(GammaDistribution, ita=1, l=2)
    run(GammaDistribution, ita=3, l=2)
    run(GammaDistribution, ita=4, l=2)
    run(GammaDistribution, ita=5, l=2)

    # run(GammaDistribution, ita=1, l=2)
    # run(GammaDistribution, ita=2, l=2)
    # run(GammaDistribution, ita=3, l=2)
    # run(GammaDistribution, ita=5, l=1)
    # run(GammaDistribution, ita=6, l=0.9)
