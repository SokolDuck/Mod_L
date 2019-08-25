from src.LR2.utils import Generator, run


class TriangularDistribution(Generator):
    DISTRIBUTION_NAME = 'Triangular distribution'
    have_ideal_example = True

    def next_random(self, *args, **kwargs):
        left_right_triangular = kwargs.get('left_right_triangular', False)

        if left_right_triangular:
            return self.a + (self.b - self.a) * min([self.random_generator.get_next_random() for _ in range(2)])
        else:
            return self.a + (self.b - self.a) * max([self.random_generator.get_next_random() for _ in range(2)])

    def ideal_example(self, sequence, *args, **kwargs):
        left_right_triangular = kwargs.get('left_right_triangular', False)

        if left_right_triangular:
            return [min(sequence), max(sequence)], [2 / (self.b -self.a), 0]
        else:
            return [min(sequence), max(sequence)], [0, 2 / (self.b -self.a)]


if __name__ == '__main__':

    run(TriangularDistribution, left_right_triangular=True)
    run(TriangularDistribution, left_right_triangular=False)

