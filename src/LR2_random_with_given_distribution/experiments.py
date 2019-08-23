import random
import matplotlib.pyplot as plt
import numpy as np


def is_prime(a):
    return not ( a < 2 or any(a % i == 0 for i in range(2, int(a ** 0.5) + 1)))


def phi(n):
    y = 1
    for i in range(2,n+1):
        if is_prime(i) is True and n % i  == 0 is True:
            y = y * (1 - 1/i)
        else:
            continue
    return int(y)


_lambda = 1
ita = 2

x = [random.random() * 20 for _ in range(1000)]
x = sorted(x)


con = (_lambda ** ita) / np.math.factorial(ita - 1)
gamma = [con * (i ** (ita - 1)) * np.e ** (-i * ita) for i in x]

_lambda = 2.75
ita = 3
con = (_lambda ** ita) / np.math.factorial(ita - 1)
gamma1 = [con * (i ** (ita - 1)) * np.e ** (-i * ita) for i in x]

_lambda = 1
ita = 5
con = (_lambda ** ita) / np.math.factorial(ita - 1)
gamma2 = [con * (i ** (ita - 1)) * np.e ** (-i * ita) for i in x]


if __name__ == '__main__':
    plt.plot(x, gamma, 'r')
    plt.plot(x, gamma1, 'g')
    plt.plot(x, gamma2, 'b')
    plt.plot(x, gamma3, 'y')
    plt.show()
