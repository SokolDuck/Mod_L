import random
import matplotlib.pyplot as plt
import numpy as np

_lambda = 1
ita = 1

x = [random.random() * 5 for _ in range(1000)]
x = sorted(x)


con = (_lambda ** ita) / np.math.factorial(ita - 1)
gamma = [con * (i ** (ita - 1)) * np.e ** (-i * ita) for i in x]

_lambda = 1.5
ita = 2
con = (_lambda ** ita) / np.math.factorial(ita - 1)
gamma1 = [con * (i ** (ita - 1)) * np.e ** (-i * ita) for i in x]

_lambda = 3
ita = 3
con = (_lambda ** ita) / np.math.factorial(ita - 1)
gamma2 = [con * (i ** (ita - 1)) * np.e ** (-i * ita) for i in x]

_lambda = 4
ita = 2
con = (_lambda ** ita) / np.math.factorial(ita - 1)
gamma3 = [con * (i ** (ita - 1)) * np.e ** (-i * ita) for i in x]

if __name__ == '__main__':
    plt.plot(x, gamma, 'r')
    plt.plot(x, gamma1, 'g')
    plt.plot(x, gamma2, 'b')
    plt.plot(x, gamma3, 'y')
    plt.show()
