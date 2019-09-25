import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pattern_A = mpimg.imread('data/A.jpg')
pattern_U = mpimg.imread('data/U.jpg')
pattern_P = mpimg.imread('data/P.jpg')

wight, height, _ = pattern_A.shape


def to_gray_scale(img):
    res = []
    in_line = img.ravel()

    res = in_line[0:-1:3]

    return np.array(res).reshape((wight, height))


pattern_A = to_gray_scale(pattern_A)
pattern_U = to_gray_scale(pattern_U)
pattern_P = to_gray_scale(pattern_P)

plt.imshow(pattern_A, cmap='gray')

pattern_A = np.where(pattern_A < 128, 1, 0)
pattern_U = np.where(pattern_U < 128, 1, 0)
pattern_P = np.where(pattern_P < 128, 1, 0)

shape = (wight, height)

net_size = wight * height


def train(patterns):
    w = []
    for pattern in patterns:
        a = pattern.ravel()
        if not w:
            w = [a[i] * a[j] if i != j else 0 for i in range(wight) for j in range(wight)]
        else:
            w = [a[i] * a[j] + w[i * 10 + j] if i != j else 0 for i in range(wight) for j in range(wight)]

    return np.array(w).reshape((wight, height))


patterns = [pattern_A, pattern_U, pattern_P]

w = train(patterns)

import random


def noise_generator(pattern, percent):
    res = np.copy(pattern)
    loc = random.sample(range(0, 100), percent)
    x = [i // 10 for i in loc]
    y = [i % 10 for i in loc]
    for i in range(0, percent):
        res[x[i], y[i]] = -pattern[x[i], y[i]]
    return res


def diff(pattern, image):
    k = 0
    for i in range(0, pattern.shape[0]):
        for j in range(0, pattern.shape[1]):
            if pattern[i, j] == image[i, j]:
                k += 1
    return (pattern.size - k) * 100 / (pattern.shape[0] * pattern.shape[1])


letters = ['A', 'U', 'P']


def recognize(patterns, image):
    min_diff, max_diff = 100, 0
    rec = 0
    for i in range(0, len(patterns)):
        d = diff(patterns[i], image)
        if d == 100 or d == 0:
            rec = i
            break
        elif d < min_diff:
            min_diff, rec = d, i
        elif d > max_diff:
            max_diff, rec = d, i
    return ['A', 'U', 'P'][rec]


noise_lavels = [i * 10 for i in range(11)]


def update(w, y_vec):
    length = len(y_vec)
    old_vec = y_vec[:]
    new_vec = np.zeros(length)
    while True:
        for i in range(0, length):
            u = 0
            for j in range(0, length):
                u += w[i, j] * old_vec[j]
            if u > 0:
                new_vec[i] = 1
            else:
                new_vec[i] = -1
        if np.array_equal(old_vec, new_vec):
            break
        new_vec, old_vec = old_vec, new_vec
    return y_vec


original = pattern_A

noise_a = [noise_generator(pattern_A, level) for level in noise_lavels for _ in range(11)]
noise_u = [noise_generator(pattern_U, level) for level in noise_lavels for _ in range(11)]
noise_p = [noise_generator(pattern_P, level) for level in noise_lavels for _ in range(11)]

if __name__ == '__main__':

    print('A')

    for num, noise in enumerate(noise_a):
        if num % 10 == 0:
            print(f'noise level = {noise_lavels[num // 10]}')

        out = update(w, noise.ravel())
        out = np.array(out).reshape(shape)
        print('Is it letter \'' + recognize(patterns, out) + '\'?')
        print('Difference:', diff(original, out), '%')
