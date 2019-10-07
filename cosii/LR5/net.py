import numpy as np


NN = 2


class Concurrent_Net:
    def __init__(self, n, m, beta):
        self.__n, self.__m, self.__Beta = n, m - NN, beta
        self.__W = np.random.uniform(0, 1, [m - NN, n])

    def train(self, origins):
        lj = len(origins) - NN
        f = np.ones(self.__m, dtype=int)
        ev = np.zeros(self.__m)

        while True:
            for j in range(lj):
                for x in range(self.__m):
                    d = 0.
                    for i in range(self.__n):
                        d += (origins[j][i] - self.__W[x, i]) ** 2
                    ev[x] = np.sqrt(d)

            dv = ev * f
            winner = dv.argmin()
            f[winner] += 1

            w = np.array(self.__W.copy())
            v = self.__W[winner] + self.__Beta * (origins[winner] - self.__W[winner])
            self.__W[winner] = v / np.sqrt(np.sum(v ** 2))

            if np.array_equal(w, self.__W):
                # print('Weights don\'t change anymore')
                return

    def recognize(self, sample):
        ev = np.zeros(self.__m)
        for j in range(self.__m):
            d = 0.
            for i in range(self.__n):
                d += (sample[i] - self.__W[j, i]) ** 2
            ev[j] = np.sqrt(d)

        return ev.argmin()

    def print_neuron(self):
        print("1, 2 - 1 neuron")
        print("3, 5 - 2 neuron")
        print("4, - 3 neuron")
