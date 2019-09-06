from cosii.LR2.utils import m_center, area, get_border
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
    center1 = m_center(labels, 1)
    v1 = area(labels, 1)
    center2 = m_center(labels, 2)
    v2 = area(labels, 2)
    center3 = m_center(labels, 3)
    v3 = area(labels, 3)
    center4 = m_center(labels, 4)
    v4 = area(labels, 4)

    border_1 = get_border(labels, 1)
    border_2 = get_border(labels, 2)
    border_3 = get_border(labels, 3)
    border_4 = get_border(labels, 4)

    plt.imshow(bin_img_obj.get_img(), cmap='gray')
    plt.scatter(center1[0], center1[1], marker='o', color='blue')
    plt.text(center1[0], center1[1], f'V(1) = {v1}', c='blue')
    plt.scatter(center2[0], center2[1], marker='o', color='red')
    plt.text(center2[0], center2[1], f'V(2) = {v2}', c='red')
    plt.scatter(center3[0], center3[1], marker='o', color='green')
    plt.text(center3[0], center3[1], f'V(3) = {v3}', c='green')
    plt.scatter(center4[0], center4[1], marker='o', color='orange')
    plt.text(center4[0], center4[1], f'V(4) = {v4}', c='orange')

    plt.scatter(list(map(lambda x: x[0], border_1)), list(map(lambda x: x[1], border_1)), s=1, color='blue')
    plt.scatter(list(map(lambda x: x[0], border_2)), list(map(lambda x: x[1], border_2)), s=1, color='red')
    plt.scatter(list(map(lambda x: x[0], border_3)), list(map(lambda x: x[1], border_3)), s=1, color='green')
    plt.scatter(list(map(lambda x: x[0], border_4)), list(map(lambda x: x[1], border_4)), s=1, color='orange')
    plt.show()


if __name__ == '__main__':
    main()
