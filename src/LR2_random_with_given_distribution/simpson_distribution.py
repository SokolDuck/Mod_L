from src.LR1.random_lemera import LemerRandomGenerator
from src.LR2_random_with_given_distribution.constants import A, B
from src.LR2_random_with_given_distribution.uniform_distribution import UniformDistribution
from src.LR2_random_with_given_distribution.utils import Generator, generate_random_sequence, build_histogram, \
    print_sequence_on_plt, get_mean_and_var, run


class SimpsonDistribution(Generator):
    def __init__(self, *args, **kwargs):
        random_generator = kwargs.get('random_generator')
        super().__init__(*args, **kwargs)
        self.uniform_distribution_gen = UniformDistribution(A / 2, B / 2, random_generator=random_generator)

    def next_random(self, *args, **kwargs):
        return sum([self.uniform_distribution_gen.next_random() for _ in range(2)])


if __name__ == '__main__':
    run(SimpsonDistribution)
