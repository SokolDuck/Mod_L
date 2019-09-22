import os

COF = {
    'e3.jpg': {
        'G': 0.2,
        'k_n': 5,
    },
    '1.jpg': {
        'G': 0.75,
        'k_n': 2,
    },
    'e1.jpg': {
        'G': 0.3,
        'k_n': 4,
    },
    'e2.jpg': {
        'G': 0.3,
        'k_n': 2,
    },
    '123.jpg': {
        'G': 0.3,
        'k_n': 2,
    },
    '2.jpg': {
        'G': 0.78,
        'k_n': 3,
    },
    '3.jpg': {
        'G': 0.8,
        'k_n': 2,
    },

}

files_list = list(COF.keys())


def get_file_path(file_name='2.jpg'):
    cur_dir = os.getcwd()

    split_path = cur_dir.split(os.path.sep)

    while split_path[-1] != 'Mod_L':
        split_path = split_path[:-1]

    coef = COF[file_name]
    G = coef.get('G')
    k_n = coef.get('k_n')

    ABSOLUT_FILE_PATH = ['cosii', 'LR2', 'data', file_name]

    split_path.extend(ABSOLUT_FILE_PATH)

    return os.path.sep.join(split_path), G, k_n


FILE_PATH, G, k_n = get_file_path()
