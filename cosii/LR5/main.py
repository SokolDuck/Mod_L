import random
import time

from cosii.LR5.image import load_images, img2bin, mat2vec, noise_generator, show
from cosii.LR5.net import Concurrent_Net

IMAGES_PATH = 'data/*.png'
BETA = 0.1

if __name__ == '__main__':
    images, names = load_images(IMAGES_PATH)
    bin_images = [img2bin(img) for img in images]

    net = Concurrent_Net(images[0].size, len(images), BETA)

    # print('Training started...')
    # start = time.time()
    net.train([mat2vec(img) for img in bin_images])
    # end = time.time()
    # print('Training finished in', format(end - start, '.1f'), 'seconds')

    for img, name in zip(bin_images, names):
        print(f'\n{name[:-3]}jpg :')
        show(img)

        for num, j in enumerate([0, 5, 10, 15, 20, 25, 30]):
            noisy = noise_generator(img, j)
            print(f'Test {num}: noise level: {j} %')
            # show(noisy)
            winner = net.recognize(mat2vec(noisy))
            print(f'Test {num}: Recognized class {winner}\n')
