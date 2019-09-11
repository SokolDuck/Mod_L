from src.LR1.constants import X0, A, M


class LemerRandomGenerator:
    def __init__(self, x0=X0, a=A, m=M, **kwargs):
        if x0 <= 1:
            x0 *= m
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
        # counter = 0
        #
        # x = self.get_next_random()
        #
        # while x != self.get_next_random():
        #     counter += 1
        #     if counter > 1_000_000:
        #         raise Exception('Period > 1_000_000')
        #
        # return counter

        V = 2 * 10 ** 6
        x_v = self.x0
        l = []
        for _ in range(V):
            x_v = self.get_next_random()
            l.append(x_v)

        self.x = None

        i1, i2 = None, None
        count = 0

        while True:
            count += 1
            next = self.get_next_random()
            if next == x_v:
                if not i1:
                    i1 = count
                elif not i2:
                    i2 = count
                else:
                    break
        P = i2 - i1

        i3 = 1
        self.x = None
        while True:
            if x_v != self.get_next_random():
                i3 += 1
            else:
                break

        aperiod = i3 + P
        return P, aperiod


if __name__ == '__main__':
    obj = LemerRandomGenerator()
    period, aperiod = obj.calculate_period()

    print(period, aperiod)

    # count = 0
    # while True:
    #     count += 1
    #     x = obj.get_next_random()
    #     x_1 = obj_p.get_next_random()
    #     if x == x_1:
    #         print(count, count + period)
    #         break
