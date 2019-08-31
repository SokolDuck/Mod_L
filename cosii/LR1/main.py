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

    # array = img.gray_scale()
    array = img.solarization()

    a = img.get_img_from_array(array)
    # a = img.gray_scale()
    plt.imshow(a, cmap='gray')
    plt.show()
    # plt.hist(array.ravel(), 255)
    # plt.show()
