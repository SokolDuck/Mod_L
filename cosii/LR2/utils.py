import numpy as np


def area(labels: np.ndarray, label_name):
    s = np.where(labels == label_name, 1, 0)
    return s.sum()


def m_center(labels: np.ndarray, label_name):
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

    return y_res, x_res


def is_inner_border(labels: np.ndarray, x, y, label_name) -> bool:
    if labels[x, y] == label_name:
        return (x != 0 and y != 0 and labels[x - 1, y - 1] != label_name) or \
               (x != 0 and labels[x - 1, y] != label_name) or \
               (x != 0 and y != labels.shape[1] and labels[x - 1, y + 1] != label_name) or \
               (y != 0 and labels[x, y - 1] != label_name) or \
               (y != labels.shape[1] and labels[x, y + 1] != label_name) or \
               (x != labels.shape[0] and y != 0 and labels[x + 1, y - 1] != label_name) or \
               (x != labels.shape[0] and labels[x + 1, y] != label_name) or \
               (x != labels.shape[0] and y != labels.shape[1] and labels[x + 1, y + 1] != label_name)

    else:
        return False


def get_border(labels: np.ndarray, label_name):
    border = []

    for y, line in enumerate(labels):
        for x, value in enumerate(line):
            if is_inner_border(labels, y, x, label_name):
                border.append((x, y))

    return border
