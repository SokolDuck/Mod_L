import os


def reload_path(_img, cat=True):
    cur_dir = os.getcwd()

    split_path = cur_dir.split(os.path.sep)

    while split_path[-1] != 'Mod_L':
        split_path = split_path[:-1]

    ABSOLUT_FILE_PATH = ['cosii', 'LR1', 'data', _img if cat else 'student.jpg']
    split_path.extend(ABSOLUT_FILE_PATH)

    FILE_PATH = os.path.sep.join(split_path)

    return FILE_PATH


FILE_PATH = reload_path('screen.jpg')
