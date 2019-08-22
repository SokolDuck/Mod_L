import numpy as np

from src.LR1.random_lemera import LemerRandomGenerator
from src.LR2_random_with_given_distribution.constants import M, SKO, N
from src.LR2_random_with_given_distribution.utils import Generator, generate_random_sequence, build_histogram, \
    print_sequence_on_plt, get_mean_and_var, run


class GaussianDistribution(Generator):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.m = kwargs.get('m', M)
        self.sko = kwargs.get('sko', SKO)
        self.n = kwargs.get('n', N)
        self.random_generator = kwargs.get('random_generator', LemerRandomGenerator())

    def next_random(self, *args, **kwargs):
        return self.m + self.sko * np.sqrt(2) * (sum([
            self.random_generator.get_next_random() for _ in range(self.n)
        ]) - self.n / 2)


if __name__ == '__main__':
    run(GaussianDistribution)
