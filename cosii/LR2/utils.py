import cv2
import numpy as np

from sklearn.cluster import KMeans


def area(labels: np.ndarray, label_name):
    s = np.where(labels == label_name, 1, 0)
    return s.sum()


def m_center(labels: np.ndarray, label_name, get_area = False):
    A = area(labels, label_name)
    x_res = 0
    y_res = 0

    for y, line in enumerate(labels):
        y_temp = []
        for x, value in enumerate(line):
            if value == label_name:
                y_temp.append(x)

        y_res += sum(y_temp)
        if y_temp != 0:
            x_res += y * len(y_temp)

    x_res /= A
    y_res /= A
    if get_area:
        return y_res, x_res, A
    else:
        return y_res, x_res


def is_inner_border(labels: np.ndarray, x, y, label_name) -> bool:
    if labels[x, y] == label_name:
        return (x != 0 and y != 0 and labels[x - 1, y - 1] != label_name) or \
               (x != 0 and labels[x - 1, y] != label_name) or \
               (x != 0 and y != labels.shape[1] - 1 and labels[x - 1, y + 1] != label_name) or \
               (y != 0 and labels[x, y - 1] != label_name) or \
               (y != labels.shape[1] - 1 and labels[x, y + 1] != label_name) or \
               (x != labels.shape[0] - 1 and y != 0 and labels[x + 1, y - 1] != label_name) or \
               (x != labels.shape[0] - 1 and labels[x + 1, y] != label_name) or \
               (x != labels.shape[0] - 1 and y != labels.shape[1] - 1 and labels[x + 1, y + 1] != label_name)

    else:
        return False


def get_border(labels: np.ndarray, label_name):
    border = []

    for y, line in enumerate(labels):
        for x, value in enumerate(line):
            if is_inner_border(labels, y, x, label_name):
                border.append((x, y))

    return border


def compactnost(border: list, area: int):
    return (len(border) ** 2) / area


def m(labels, label_name, i, j):
    m_y, m_x, a = m_center(labels, label_name, get_area=True)

    m = 0

    for x in range(labels.shape[0]):
        for y in range(labels.shape[1]):
            if labels[x, y] == label_name:
                temp = ((x - m_x) ** i) * ((y - m_y) ** j)
                m += temp

    return m


def elongation(labels, label_name):
    m_2_0 = m(labels, label_name, 2, 0)
    m_0_2 = m(labels, label_name, 0, 2)
    m_1_1 = m(labels, label_name, 1, 1)
    sq = np.sqrt((m_2_0 - m_0_2) ** 2 + 4 * m_1_1 ** 2)

    return (m_2_0 + m_0_2 + sq) / \
           (m_2_0 + m_0_2 - sq)


def k_mean(vectors, n_clusters=2):
    if not isinstance(vectors, np.ndarray):
        vectors = np.array(vectors)
    km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1,
                verbose=False)
    km.fit(vectors)
    return km


def get_class(vector, km):
    return int(km.predict(np.array(vector))[0])


def blur(img: np.ndarray):

    blur = cv2.GaussianBlur(img, (5, 5), 0)

    return img
