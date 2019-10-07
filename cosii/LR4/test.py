import numpy as np

from cosii.LR3.images import noise_generator
from cosii.LR4.const import I_Q, I_W, I_V, I_T
from cosii.LR4.data.classes import class1, class5, class4, class3, class2

classes = [class1, class2, class3, class4, class5]

answers = [
    np.array([1, 0, 0, 0, 0]),
    np.array([0, 1, 0, 0, 0]),
    np.array([0, 0, 1, 0, 0]),
    np.array([0, 0, 0, 1, 0]),
    np.array([0, 0, 0, 0, 1])
]

x_y = list(zip(classes, answers))


def nonlin(x, deriv=False):
    if deriv:
        return x * (1 - x)
    else:
        return 1 / (1 + np.exp(-x))


def show(image):
    print('\n'.join(''.join(' ' if cell == 0 else 'X' for cell in row) for row in image))
    print()


h = 16
n = 36
m = 5


def train(W, V, T, Q, D):
    for i in range(1_000_000):
        d_max = []
        if i % 10_000 == 0:
            print(f'\niteration № {i // 10000}0 000')

        for i_x_y in x_y:
            _in, _out = i_x_y

            x = _in.ravel()

            g = np.array([nonlin(sum(V[:, num] * x) + Q[num]) for num in range(h)])
            y = np.array([nonlin(sum(W[:, num] * g) + T[num]) for num in range(m)])

            d = _out - y
            d_max.extend(d)

            if i % 10000 == 0:
                print(f'ошибка d = {d}')
                print(f'y = {y}, check = {_out}')

            y_delta = d * nonlin(y, deriv=True)

            g_error = y_delta.dot(W.T)

            g_delta = g_error * nonlin(g, deriv=True)

            W += g.reshape(16, 1).dot(y_delta.reshape(1, 5))
            V += x.reshape(36, 1).dot(g_delta.reshape(1, 16))

        if max(d_max) < D:
            print('done')
            print('W')
            print(W)
            print('V')
            print(V)
            print('Q')
            print(Q)
            print('T')
            print(T)

            return None

    print('not done')
    print(d_max)


def predict(_in, W, V, T, Q):
    x = _in.ravel()

    g = np.array([nonlin(sum(V[:, num] * x) + Q[num]) for num in range(h)])
    y = np.array([nonlin(sum(W[:, num] * g) + T[num]) for num in range(m)])

    return y


def save_():
    pass


def load_():

    pass


def test_predict(_in, _out, W, V, T, Q):
    mes = [
        'class 1',
        'class 2',
        'class 3',
        'class 4',
        'class 5',
    ]

    answer = ''.join([mes[i] * _out[i] for i in range(len(mes))])

    print(f'we try to predict {answer}')

    y = predict(_in, W, V, T, Q)

    for num, ys in enumerate(y):
        print(f'{mes[num]} = {round(ys * 100, 2)}%')


def with_train():
    # h*n
    V = 2 * np.random.random((n, h)) - 1

    Q = np.random.random(h)

    # h*m
    W = 2 * np.random.random((h, m)) - 1

    T = np.random.random(m)

    train(W, V, T, Q, D=0.01)

    noises = [10 * i for i in range(3)]

    for noise in noises:
        print(f'\nwith noise {noise}%')
        without_train(noise, W, V, T, Q)


def without_train(noise=None, W=None, V=None, T=None, Q=None):
    if noise:
        for _x_y in x_y:
            no = noise_generator(_x_y[0].copy(), noise)
            show(no)
            if W is None:
                test_predict(no, _x_y[1], I_W, I_V, I_T, I_Q)
            else:
                test_predict(no, _x_y[1], W, V, T, Q)
    else:
        for _x_y in x_y:
            if W is None:
                test_predict(_x_y[0], _x_y[1], I_W, I_V, I_T, I_Q)
            else:
                test_predict(_x_y[0], _x_y[1], W, V, T, Q)


if __name__ == '__main__':
    with_train()
    # noises = [10 * i for i in range(3)]
    # for noise in noises:
    #     print(f'\nwith noise {noise}%')
    #     without_train(noise=noise)

    # for _class in classes:
    #     show(_class)
