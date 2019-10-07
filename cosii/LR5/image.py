import random
import imageio
import glob
import numpy as np
import os


def img2bin(x):
    y = np.ndarray((x.shape[0], x.shape[1]), dtype=int)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            y[i, j] = 0 if x[i, j] == 0 else 1
    return y


def bin2img(x):
    y = np.ndarray((x.shape[0], x.shape[1]), dtype=int)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            y[i, j] = 0 if x[i, j] == 0 else 255
    return y


def mat2vec(x):
    vec = np.zeros(x.size, dtype=int)
    c = 0
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            vec[c] = x[i, j]
            c += 1
    return vec


def vec2mat(x, w=10, h=10):
    mat = np.array(x).copy()
    mat.resize(w, h)
    return mat


def diff(pattern, img):
    k = 0
    for i in range(pattern.shape[0]):
        for j in range(pattern.shape[1]):
            if pattern[i, j] == img[i, j]:
                k += 1
    return (pattern.size - k) * 100 / (pattern.shape[0] * pattern.shape[1])


def load_images(path):
    pictures, names = [], []

    for image_path in glob.glob(path):
        im = imageio.imread(image_path)
        imm = []
        for num, line in enumerate(im):
            imm.append([])
            for i, item in enumerate(line):
                imm[num].append(item[0])

        pictures.append(np.array(imm))
        names.append(os.path.split(image_path)[-1])

    return pictures, names


def noise_generator(img, percent):
    res = np.array(img).copy()
    num = percent * img.size // 100
    loc = random.sample(range(img.size), num)
    xy = [(i // img.shape[0], i % img.shape[1]) for i in loc]
    for i in xy:
        res[i] = 1 if img[i] == 0 else 0
    return res


def show(img):
    print('\n'.join(''.join('X' if cell == 0 else ' ' for cell in row) for row in img))
