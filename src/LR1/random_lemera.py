from src.LR1.constants import X0, A, M


class LemerRandomGenerator:
    def __init__(self, x0=X0, a=A, m=M, **kwargs):
        self.x0 = x0
        self.a = a
        self.m = m
        self.x = None

    def get_next_random(self):
        self.x = self.a * (self.x or self.x0) % self.m
        return self.x / self.m

    def get_random_num(self, x: int = None, a: int = None, m: int = None):
        return (a or self.a) * (x or self.x or self.x0) % (m or self.m)

    def calculate_period(self):
        counter = 0

        x = self.get_next_random()

        while x != self.get_next_random():
            counter += 1
            if counter > 1_000_000:
                raise Exception('Period > 1_000_000')

        return counter
