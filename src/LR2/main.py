from src.LR2.distribution.exponential_distribution import ExponentialDistribution
from src.LR2.distribution.gamma_distribution import GammaDistribution
from src.LR2.distribution.gaussian_distribution import GaussianDistribution
from src.LR2.distribution.simpson_distribution import SimpsonDistribution
from src.LR2.distribution.triangular_distribution import TriangularDistribution
from src.LR2.distribution.uniform_distribution import UniformDistribution
from src.LR2.utils import run


if __name__ == '__main__':
    run(UniformDistribution)

    run(TriangularDistribution, left_right_triangular=True)
    run(TriangularDistribution, left_right_triangular=False)

    run(SimpsonDistribution)

    run(GaussianDistribution)

    run(ExponentialDistribution, l=0.5)
    run(ExponentialDistribution, l=1)
    run(ExponentialDistribution, l=1.5)

    run(GammaDistribution, l=1, ita=2)
