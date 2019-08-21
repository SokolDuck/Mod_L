from src.LR2_random_with_given_distribution.gaussian_distribution import GaussianDistribution
from src.LR2_random_with_given_distribution.simpson_distribution import SimpsonDistribution
from src.LR2_random_with_given_distribution.triangular_distribution import TriangularDistribution
from src.LR2_random_with_given_distribution.uniform_distribution import UniformDistribution
from src.LR2_random_with_given_distribution.utils import run

if __name__ == '__main__':
    run(UniformDistribution)

    run(TriangularDistribution, left_right_triangular=True)
    run(TriangularDistribution, left_right_triangular=False)

    run(SimpsonDistribution)

    run(GaussianDistribution)
