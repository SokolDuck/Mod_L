import numpy as np

from cosii.LR1.image_corrector import ImageCorrector
import matplotlib.pyplot as plt

from cosii.LR1.constants import FILE_PATH

if __name__ == '__main__':
    img = ImageCorrector(file_path=FILE_PATH)
    # plt.hist(img.ravel, 255)
    # plt.show()
    # plt.imshow(img.get_img())
    # plt.show()

    # array = img.image_preparation('a', border=100)
    # array = img.image_preparation('b', left=50, right=150)
    # array = img.image_preparation('c', a=150)
    # array = img.image_preparation('d', a=100)
    # array = img.image_preparation('e', a=70)
    # array = img.image_preparation('f', a=70)

    # array = img.solarization()

    # a = img.get_img_from_array(array)
    # a = img.gray_scale()

    # низкочастотные
    h1 = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]) / 9
    h2 = np.array([
        [1, 1, 1],
        [1, 2, 1],
        [1, 1, 1],
    ]) / 10
    h3 = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1],
    ]) / 16

    # высокочастотные
    h1_1 = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1],
    ])
    h2_2 = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ])
    h3_3 = np.array([
        [1, -2, 1],
        [-2, 5, -2],
        [1, -2, 1],
    ])

    a = img.use_filter(h1_1)
    plt.imshow(a, cmap='gray')
    plt.show()
    a = img.use_filter(h2_2)
    plt.imshow(a, cmap='gray')
    plt.show()
    a = img.use_filter(h3_3)
    plt.imshow(a, cmap='gray')
    plt.show()
    # plt.hist(array.ravel(), 255)
    # plt.show()
