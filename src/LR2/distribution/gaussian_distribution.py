import numpy as np
from scipy.stats import norm

from src.LR1.random_lemera import LemerRandomGenerator
from src.LR2.constants import MU, SIGMA, N, COUNT
from src.LR2.utils import Generator, run


class GaussianDistribution(Generator):
    DISTRIBUTION_NAME = 'Gaussian distribution'
    have_ideal_example = True

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.mu = kwargs.get('mu', MU)
        self.sigma = kwargs.get('sigma', SIGMA)
        self.n = kwargs.get('n', N)
        self.random_generator = kwargs.get('random_generator', LemerRandomGenerator())

    def next_random(self, *args, **kwargs):
        return self.mu + self.sigma * np.sqrt(2) * (sum([
            self.random_generator.get_next_random() for _ in range(self.n)
        ]) - self.n / 2)

    @property
    def params(self):
        return r'mu = {}, sigma = {}, n = {}'.format(self.mu, self.sigma, self.n)

    def ideal_example(self, bins, N=COUNT, **kwargs):
        x = sorted(bins)
        return x, norm.pdf(x, self.mu, self.sigma)


if __name__ == '__main__':
    run(GaussianDistribution)
