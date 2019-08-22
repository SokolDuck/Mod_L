from src.LR2_random_with_given_distribution.distribution.exponential_distribution import ExponentialDistribution
from src.LR2_random_with_given_distribution.distribution.gaussian_distribution import GaussianDistribution
from src.LR2_random_with_given_distribution.distribution.simpson_distribution import SimpsonDistribution
from src.LR2_random_with_given_distribution.distribution.triangular_distribution import TriangularDistribution
from src.LR2_random_with_given_distribution.distribution.uniform_distribution import UniformDistribution
from src.LR2_random_with_given_distribution.utils import run


if __name__ == '__main__':
    run(UniformDistribution)

    run(TriangularDistribution, left_right_triangular=True)
    run(TriangularDistribution, left_right_triangular=False)

    run(SimpsonDistribution)

    run(GaussianDistribution)

    run(ExponentialDistribution, l=0.5)
    run(ExponentialDistribution, l=1)
    run(ExponentialDistribution, l=1.5)
