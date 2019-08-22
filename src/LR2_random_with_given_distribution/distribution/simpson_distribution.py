import numpy as np

from src.LR2_random_with_given_distribution.constants import A, B
from src.LR2_random_with_given_distribution.distribution.uniform_distribution import UniformDistribution
from src.LR2_random_with_given_distribution.utils import Generator, run

from scipy.integrate import simps


class SimpsonDistribution(Generator):
    DISTRIBUTION_NAME = 'Simpson distribution'
    have_ideal_example = True

    def __init__(self, *args, **kwargs):
        random_generator = kwargs.get('random_generator')
        super().__init__(*args, **kwargs)
        self.uniform_distribution_gen = UniformDistribution(A / 2, B / 2, random_generator=random_generator)

    def next_random(self, *args, **kwargs):
        return sum([self.uniform_distribution_gen.next_random() for _ in range(2)])

    def ideal_example(self, seq, *args, **kwargs):
        a = min(seq)
        b = max(seq)
        return [a, self.a, (a + b) / 2, self.b, b], [0, 0, 2 / (b - a), 0, 0]


if __name__ == '__main__':
    run(SimpsonDistribution)
