from src.LR2.utils import Generator, run


class UniformDistribution(Generator):
    DISTRIBUTION_NAME = 'Uniform distribution'
    have_ideal_example = True

    def mean(self):
        return (self.a + self.b) / 2

    def var(self):
        return (self.b - self.a) ** 2 / 12

    def next_random(self, *args, **kwargs):
        return self.a + (self.b - self.a) * self.random_generator.get_next_random()

    def ideal_example(self, sequence, *args, **kwargs):
        return [self.a, self.b], [1 / (self.b - self.a), 1 / (self.b - self.a)]


if __name__ == '__main__':
    run(UniformDistribution)
