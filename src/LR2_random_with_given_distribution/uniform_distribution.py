from src.LR2_random_with_given_distribution.utils import (Generator, run)


class UniformDistribution(Generator):
    def mean(self):
        return (self.a + self.b) / 2

    def var(self):
        return (self.b - self.a) ** 2 / 12

    def next_random(self):
        return self.a + (self.b - self.a) * self.random_generator.get_next_random()


if __name__ == '__main__':
    run(UniformDistribution)
