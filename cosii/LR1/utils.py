import matplotlib.image as mpimg
import numpy as np


class ImageGenerator:
    def __init__(self, img: np.ndarray = None, file_path=None):
        self.img = img
        self.file_path = file_path

        if file_path and not img:
            self.img, self.ravel = get_img(file_path)
        else:
            self.ravel = self.img.ravel()
        # if self.ravel.size > self.img.shape[0] * self.img.shape[1]:
        #     self.ravel = np.array([self.ravel[i] for i in range(0, self.ravel.size, self.img.shape[2])])

        self.x_min, self.x_max = min(self.ravel), max(self.ravel)
        self.img_cor = self.img

    def get_img(self, img: np.ndarray = None):
        return np.array(img) if img else self.img

    def get_img_as_array(self):
        return self.ravel

    def get_next_random(self, *args, **kwargs):
        for item in self.ravel:
            yield item

    def linear_correction(self, y_min, y_max):
        kof_a = (y_max - y_min) / (self.x_max - self.x_min)
        kof_b = y_max - kof_a * self.x_max

        if not isinstance(self.x_min, int):
            y_min /= 255
            y_max /= 255
            kof_a /= 255
            kof_b /= 255

        # return ((self.ravel - self.x_min) * (y_max - y_min) / (self.x_max - self.x_min)) + y_min

        return kof_a * self.ravel + kof_b
        # return (a * self.ravel + b) % 256 / 255

    def get_img_from_array(self, array: np.ndarray):
        if len(self.img.shape) == 3:
            img = array.reshape((self.img.shape[0], self.img.shape[1], self.img.shape[2]))
        else:
            img = array.reshape((self.img.shape[0], self.img.shape[1]))
        return img


def get_img(file_path:str):
    img = mpimg.imread(file_path)

    return img, img.ravel()
