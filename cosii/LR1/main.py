from PIL import Image
from src.LR2.utils import build_histogram
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from cosii.LR1.constants import FILE_PATH

if __name__ == '__main__':
    # img = Image.open(FILE_PATH)
    # data = list(img.getdata(0))
    img = mpimg.imread(FILE_PATH)


    plt.imshow(img, cmap='gray')
    plt.show()
    data = img.ravel()

    build_histogram(data, 255)

    # img.show()