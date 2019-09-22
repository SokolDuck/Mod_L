import numpy as np


def train(images):
    count = len(images[0])
    w = np.zeros([count, count])
    for i in range(0, count):
        for j in range(0, count):
            if i == j:
                w[i, j] = 0
            else:
                for image in images:
                    w[i, j] += image[i] * image[j]
                w[j, i] = w[i, j]
    return w


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
