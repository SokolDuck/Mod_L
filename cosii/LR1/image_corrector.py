from collections import defaultdict

import numpy as np

from cosii.LR1.utils import get_img


# Use only jpg images
class ImageCorrector:
    def __init__(self, img: np.ndarray = None, file_path=None):
        self.img = img
        self.file_path = file_path

        if file_path and not img:
            self.img, self.ravel = get_img(file_path)
        else:
            self.ravel = self.img.ravel()

        if self.ravel[0] <= 1:
            self.ravel *= 255

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
            kof_a /= 255
            kof_b /= 255

        # return ((self.ravel - self.x_min) * (y_max - y_min) / (self.x_max - self.x_min)) + y_min
        return kof_a * self.ravel + kof_b
        # return (a * self.ravel + b) % 256 / 255

    def gamma_correction(self, A, y):
        if self.ravel[0] > 1:
            return A * ((self.ravel / 255) ** y)
        else:
            return A * (self.ravel ** y)

    def logarithmic_correction(self, c):
        if self.ravel[0] > 1:
            return np.array([c * np.log10(1 + i) for i in self.ravel])
        else:
            return c * np.log10(1 + self.ravel * 255)

    def image_preparation(self, type: str, **kwargs):
        """
        :param type: str a, b, c, d, e, f
        - a - binary preparation
        - b - lightning slice
        - c - downstream lights
        - d - upstream lights
        - e - upstream contrast
        - f - downstream contrast
        :param args:
            a:
            - border: int
            b:
            - left: int
            - right: int
            c:
            - a: int
            d:
            - a: int
            e, f:
            - a: int
        :return: np.ndarray
        """
        img = self.ravel
        if type == 'a':
            img = np.where(self.ravel > kwargs.get('border'), 255, 0)
        elif type == 'b':
            img = np.where((kwargs.get('left') < self.ravel) == (self.ravel < kwargs.get('right')), 255, 0)
        elif type == 'c':
            img = np.where(self.ravel < kwargs.get('a'), self.ravel - kwargs.get('a'), 0)
            img = np.where(img == 255 - kwargs.get('a'), 255, img)
        elif type == 'd':
            img = np.where(self.ravel < 255 - kwargs.get('a'), self.ravel + kwargs.get('a'), 255)
        elif type == 'e':
            a = kwargs.get('a')
            r = a + (self.ravel / 255) * (255 - 2 * a)
            img = np.where((self.ravel != 0) == (self.ravel != 255), r, self.ravel)
            img = np.where(img == 0, a, img) / 255
        elif type == 'f':
            a = kwargs.get('a')
            img = np.where(self.ravel < a, 0, self.ravel)
            img = np.where(img > 255 - a, 255, img)
            r = a + (self.ravel / 255) * (255 - 2 * a)
            img = np.where((img != 0) == (img != 255), r, img) / 255
        return img

    def negative(self):
        return 255 - self.ravel

    def gray_scale(self):
        img = []
        for line in self.img:
            l = []
            for col in line:
                l.append((0.11 * col[0] + 0.59 * col[1] + 0.3 * col[2]) / 255)
            img.append(l)

        return np.array(img)

    def solarization(self, k=1):
        k = 4 / self.x_max
        return (k * self.ravel * (self.x_max - self.ravel)) / 255

    def get_img_from_array(self, array: np.ndarray):
        if len(self.img.shape) == 3:
            img = array.reshape((self.img.shape[0], self.img.shape[1], self.img.shape[2]))
        else:
            img = array.reshape((self.img.shape[0], self.img.shape[1]))
        return img

    def use_filter(self, h: np.ndarray):
        img = np.copy(self.img) / 255

        if len(h.shape) == 3:
            img = self.gray_scale()

        if h.shape[0] == h.shape[1] and h.shape[0] == 3:
            for row, line in enumerate(img[1: -1]):
                for col, pixel in enumerate(line[1: -1]):
                    img[row + 1, col + 1] = (img[row: row + 3, col: col + 3] * h).sum()
        else:
            raise Exception('not valid filters mask')

        return img

    def linked_spaces(self, labels=None, recurs: bool = False):
        if not labels:
            labels = np.copy(self.img) * 0

        label = 0
        eq = {}

        for x in range(self.img.shape[0]):
            for y in range(self.img.shape[1]):
                if recurs:
                    self._fill(labels, x, y, label)
                    label += 1
                else:
                    if self.img[x, y] == 0:
                        if labels[x - 1, y] == 0 and labels[x, y - 1] == 0:
                            label += 1
                            labels[x, y] = label
                        if labels[x - 1, y] != 0 and labels[x, y - 1] != 0 and labels[x - 1, y] == labels[x, y - 1]:
                            labels[x, y] = labels[x - 1, y]
                        elif labels[x - 1, y] != 0 and labels[x, y - 1] != 0:
                            eq[labels[x - 1, y]] = labels[x, y - 1]
                            labels[x, y] = labels[x - 1, y]
                        elif labels[x - 1, y] != 0:
                            labels[x, y] = labels[x - 1, y]
                        elif labels[x, y - 1] != 0:
                            labels[x, y] = labels[x, y - 1]

        keys = list(eq.keys())
        mark = 1
        relationship = defaultdict(list)
        k = keys[0]

        while True:
            v = eq.get(k)
            if eq.get(v):
                if k not in relationship[mark]:
                    keys.remove(k)
                    relationship[mark].append(k)

                relationship[mark].append(v)
                if v in keys:
                    keys.remove(v)
                if len(keys) == 0:
                    relationship[mark].append(eq.get(v))
                    break
                k = v
            else:
                relationship[mark].append(v)
                mark += 1
                k = keys[0]

        for l, r in relationship.items():
            for key in r:
                labels[labels == key] = l

        if labels.max == mark - 1:
            return labels
        else:
            labels[labels == labels.max()] = mark
            return labels

    def _fill(self, labels, x, y, label):
        if labels[x, y] == 0 and self.img[x, y] == 255:
            labels[x, y] = label
            if x > 0:
                self._fill(labels, x - 1, y, label)
            if x < self.img.shape[1] - 1:
                self._fill(labels, x + 1, y, label)
            if y > 0:
                self._fill(labels, x, y - 1, label)
            if y < self.img.shape[0] - 1:
                self._fill(labels, x, y + 1, label)
