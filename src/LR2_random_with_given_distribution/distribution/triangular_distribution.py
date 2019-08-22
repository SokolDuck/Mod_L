from src.LR1.random_lemera import LemerRandomGenerator
from src.LR2_random_with_given_distribution.utils import (Generator, build_histogram, print_sequence_on_plt,
                                                          get_mean_and_var, generate_random_sequence, run)


class TriangularDistribution(Generator):
    def next_random(self, *args, **kwargs):
        left_right_triangular = kwargs.get('left_right_triangular', False)

        if left_right_triangular:
            return self.a + (self.b - self.a) * min([self.random_generator.get_next_random() for _ in range(2)])
        else:
            return self.a + (self.b - self.a) * max([self.random_generator.get_next_random() for _ in range(2)])


if __name__ == '__main__':

    run(TriangularDistribution, left_right_triangular=True)
    run(TriangularDistribution, left_right_triangular=False)

