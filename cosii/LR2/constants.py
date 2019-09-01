import os

cur_dir = os.getcwd()

split_path = cur_dir.split(os.path.sep)

while split_path[-1] != 'Mod_L':
    split_path = split_path[:-1]

ABSOLUT_FILE_PATH = ['cosii', 'LR2', 'data', 'lr2.jpg']

split_path.extend(ABSOLUT_FILE_PATH)

FILE_PATH = os.path.sep.join(split_path)
