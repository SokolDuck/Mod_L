from functools import reduce

import numpy as np
import math

from src.LR2_random_with_given_distribution.constants import LAMBDA, ITA
from src.LR2_random_with_given_distribution.utils import Generator


class GammaDistribution(Generator):
    DISTRIBUTION_NAME = 'Gamma distribution'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._lambda = kwargs.get('l', LAMBDA)
        self.ita = kwargs.get('ita', ITA)

    def next_random(self, *args, **kwargs):
        return -1 / self._lambda * np.log(reduce(lambda x, y: x * y,
                                                 [self.random_generator.get_next_random() for _ in range(self.ita)]))

    def ideal_example(self, sequence, *args, **kwargs):
        x = sorted(sequence)

        con = (self._lambda ** self.ita) / math.factorial(self.ita - 1)

        return x, [con * (i ** (self.ita - 1)) * np.exp(-self.ita * )]