from cosii.LR1.image_corrector import ImageCorrector
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
    labels *= 50
    labels[labels == 0] = 255
    plt.imshow(labels, cmap='gray')
    plt.show()


if __name__ == '__main__':
    main()
