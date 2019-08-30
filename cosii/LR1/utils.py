import matplotlib.image as mpimg


def get_img(file_path:str):
    img = mpimg.imread(file_path)

    return img, img.ravel()
