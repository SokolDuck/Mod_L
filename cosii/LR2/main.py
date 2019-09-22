import numpy as np

from cosii.LR2.utils import m_center, area, get_border, elongation, k_mean, get_class, blur
from cosii.image_corrector import ImageCorrector
from cosii.LR2.constants import FILE_PATH, get_file_path, files_list

import matplotlib.pyplot as plt

COLORS = ['red', 'green', 'blue', 'orange', 'yellow']


def main(file_name=None):
    if not file_name:
        img_obj = ImageCorrector(file_path=FILE_PATH)
        from cosii.LR2.constants import G, k_n
    else:
        path, G, k_n = get_file_path(file_name)
        img_obj = ImageCorrector(file_path=path)

    h1 = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]) / 9

    plt.imshow(img_obj.get_img(), cmap='gray')
    plt.show()

    gray_scale = img_obj.gray_scale()

    img_obj = ImageCorrector(img=gray_scale)
    img_obj.img = img_obj.use_filter(h1) * 255
    img_obj.img = img_obj.use_filter(h1) * 255
    img_obj.img = img_obj.get_img_from_array(img_obj.gamma_correction(1, 3))

    plt.imshow(img_obj.get_img(), cmap='gray')
    plt.show()

    bin_array = img_obj.image_preparation('a', border=G)
    bin_img = img_obj.get_img_from_array(bin_array)
    plt.imshow(bin_img, cmap='gray')
    plt.show()

    # bin_img = blur(bin_img)
    #
    # plt.imshow(bin_img, cmap='gray')
    # plt.show()
    bin_img_obj = ImageCorrector(img=bin_img)
    labels = bin_img_obj.linked_spaces()

    objects = []
    centers = []
    borders = []
    elevations = []
    for i in range(labels.max()):
        v = area(labels, i + 1)
        if v > 100:
            centers.append(m_center(labels, i + 1))
            objects.append(v)
            borders.append(get_border(labels, i + 1))
            elevations.append(elongation(labels, i + 1))

    plt.imshow(bin_img_obj.get_img(), cmap='gray')

    for num, center in enumerate(centers):
        if objects[num] > 100:
            plt.scatter(center[0], center[1], marker='o', color='blue')
            plt.text(center[0], center[1], f'V({num}) = {objects[num]}', c='blue')
            plt.text(center[0], center[1] + 20, f'E({num}) = {int(elevations[num])}', c='blue')

    for num, border in enumerate(borders):
        if objects[num] > 100:
            plt.scatter(list(map(lambda x: x[0], border)), list(map(lambda x: x[1], border)), s=1, color='red')

    plt.show()

    vectors = list(zip(objects, elevations))
    km = k_mean(vectors, k_n)

    plt.imshow(bin_img_obj.get_img(), cmap='gray')
    classes = km.predict(vectors)

    for num in range(len(objects)):
        color = COLORS[classes[num]]
        center = centers[num]
        plt.text(center[0], center[1], f'V({num}) = {objects[num]}', c=color)
        plt.scatter(list(map(lambda x: x[0], borders[num])), list(map(lambda x: x[1], borders[num])), s=1, color=color)

    plt.show()


if __name__ == '__main__':
    # for file_name in files_list:
    main('3.jpg')
