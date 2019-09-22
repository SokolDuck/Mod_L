import random
import numpy as np

letters = ['В', 'Т', 'Л']

# изображение буквы 'В'
pattern0 = np.array([[+1, +1, -1, -1, -1, -1, -1, +1, +1, +1],
                     [+1, +1, -1, -1, -1, -1, +1, +1, +1, +1],
                     [+1, +1, -1, -1, -1, -1, +1, +1, +1, +1],
                     [+1, +1, -1, -1, -1, +1, +1, -1, +1, +1],
                     [+1, +1, -1, -1, +1, +1, -1, -1, +1, +1],
                     [+1, +1, -1, -1, +1, +1, -1, -1, +1, +1],
                     [+1, +1, -1, +1, +1, -1, -1, -1, +1, +1],
                     [+1, +1, +1, +1, +1, -1, -1, -1, +1, +1],
                     [+1, +1, +1, +1, -1, -1, -1, -1, +1, +1],
                     [+1, +1, +1, -1, -1, -1, -1, -1, +1, +1]])

# изображение буквы 'Т'
pattern1 = np.array([[+1, +1, +1, +1, +1, +1, +1, +1, +1, +1],
                     [+1, +1, +1, +1, +1, +1, +1, +1, +1, +1],
                     [+1, +1, +1, +1, +1, +1, +1, +1, +1, +1],
                     [-1, -1, -1, +1, +1, +1, -1, -1, -1, -1],
                     [-1, -1, -1, +1, +1, +1, -1, -1, -1, -1],
                     [-1, -1, -1, +1, +1, +1, -1, -1, -1, -1],
                     [-1, -1, -1, +1, +1, +1, -1, -1, -1, -1],
                     [-1, -1, -1, +1, +1, +1, -1, -1, -1, -1],
                     [-1, -1, -1, +1, +1, +1, -1, -1, -1, -1],
                     [-1, -1, -1, +1, +1, +1, -1, -1, -1, -1]])

# изображение буквы 'Л'
pattern2 = np.array([[-1, +1, +1, +1, +1, +1, +1, +1, +1, +1],
                     [-1, +1, +1, +1, +1, +1, +1, +1, +1, +1],
                     [-1, +1, +1, +1, -1, -1, -1, +1, +1, +1],
                     [-1, +1, +1, +1, -1, -1, -1, +1, +1, +1],
                     [-1, +1, +1, +1, -1, -1, -1, +1, +1, +1],
                     [-1, +1, +1, +1, -1, -1, -1, +1, +1, +1],
                     [-1, +1, +1, +1, -1, -1, -1, +1, +1, +1],
                     [-1, +1, +1, +1, -1, -1, -1, +1, +1, +1],
                     [-1, +1, +1, +1, -1, -1, -1, +1, +1, +1],
                     [+1, +1, +1, -1, -1, -1, -1, +1, +1, +1]])

patterns = [pattern0, pattern1, pattern2]


def noise_generator(pattern, percent):
    res = np.copy(pattern)
    loc = random.sample(range(0, 100), percent)
    x = [i // 10 for i in loc]
    y = [i % 10 for i in loc]
    for i in range(0, percent):
        res[x[i], y[i]] = -pattern[x[i], y[i]]
    return res


def show(image):
    print('\n'.join(''.join(' ' if cell == -1 else 'X' for cell in row) for row in image))
    print()


def diff(pattern, image):
    k = 0
    for i in range(0, pattern.shape[0]):
        for j in range(0, pattern.shape[1]):
            if pattern[i, j] == image[i, j]:
                k += 1
    return (pattern.size - k) * 100 / (pattern.shape[0] * pattern.shape[1])


def mat2vec(x):
    m = x.shape[0] * x.shape[1]
    vec = np.zeros(m)
    c = 0
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            vec[c] = x[i, j]
            c += 1
    return vec


def vec2mat(x, w=10, h=10):
    a = np.array(x).copy()
    a.resize(w, h)
    return a


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
    return letters[rec]


if __name__ == '__main__':
    test = noise_generator(pattern0, 60)
    show(pattern0)
    print()
    show(test)
    print(diff(pattern0, test), '%')
