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
        if self.ravel.size > self.img.shape[0] * self.img.shape[1]:
            self.ravel = np.array([self.ravel[i] for i in range(0, self.ravel.size, 3)])

        self.f_min, self.f_max = min(self.ravel), max(self.ravel)
        self.img_cor = self.img

    def get_img(self, img: np.ndarray = None):
        return np.array(img) if img else self.img

    def get_img_as_array(self):
        return self.ravel

    def get_next_random(self, *args, **kwargs):
        for item in self.ravel:
            yield item

    def linear_correction(self, a, b):
        # return ((self.ravel - self.f_min) * 100 / (self.f_max - self.f_min)) + 100
        return 0.48 * self.ravel + 98
        # return (a * self.ravel + b) % 256 / 255

    def get_img_from_array(self, array: np.ndarray):
        img = array.reshape((self.img.shape[0], self.img.shape[1]))
        return img


def get_img(file_path:str):
    img = mpimg.imread(file_path)

    return img, img.ravel()
