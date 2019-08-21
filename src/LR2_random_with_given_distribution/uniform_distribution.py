from src.LR2_random_with_given_distribution.utils import (Generator, generate_random_sequence, get_mean_and_var,
                                                          build_histogram, print_sequence_on_plt)


class UniformDistribution(Generator):
    def mean(self):
        return (self.a + self.b) / 2

    def var(self):
        return (self.b - self.a) ** 2 / 12

    def next_random(self):
        self.x = self.a + (self.b - self.a) * self.x
        return self.x


if __name__ == '__main__':

    generator_obj = UniformDistribution()
    seq = generate_random_sequence(generator_obj)

    build_histogram(seq)
    print_sequence_on_plt(seq)
    get_mean_and_var(generator_obj, seq)