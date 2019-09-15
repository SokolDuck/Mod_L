from cosii.LR2.utils import m_center, area, get_border, elongation, k_mean, get_class
from cosii.image_corrector import ImageCorrector
from cosii.LR2.constants import FILE_PATH

import matplotlib.pyplot as plt


def main():
    img_obj = ImageCorrector(file_path=FILE_PATH)
    plt.imshow(img_obj.get_img(), cmap='gray')
    plt.show()

    gray_scale = img_obj.gray_scale()

    img_obj = ImageCorrector(img=gray_scale)
    plt.imshow(img_obj.get_img(), cmap='gray')
    plt.show()

    bin_array = img_obj.image_preparation('a', border=200)
    bin_img = img_obj.get_img_from_array(bin_array)
    plt.imshow(bin_img, cmap='gray')
    plt.show()

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
    km = k_mean(vectors)

    plt.imshow(bin_img_obj.get_img(), cmap='gray')
    classes = km.predict(vectors)

    for num in range(len(objects)):
        color = 'blue' if classes[num] == 0 else 'red'
        center = centers[num]
        plt.text(center[0], center[1], f'V({num}) = {objects[num]}', c=color)
        plt.scatter(list(map(lambda x: x[0], borders[num])), list(map(lambda x: x[1], borders[num])), s=1, color=color)

    plt.show()


if __name__ == '__main__':
    main()
