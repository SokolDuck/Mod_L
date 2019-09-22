import cosii.LR3.images as img
import cosii.LR3.hopfield as hp


def main():
    vectors = [pattern.ravel() for pattern in img.patterns]
    w = hp.train(vectors)

    n = int(input('Number of pattern(0 - 2): '))
    original = img.patterns[n]
    print('Original image:')
    img.show(original)

    noise_percent = int(input('Noise percent(0 - 100): '))
    noisy = img.noise_generator(original, noise_percent)
    img.show(noisy)

    y_vec = noisy.ravel()
    y_vec = hp.update(w, y_vec)
    out = img.vec2mat(y_vec)

    print('\nResult Image:')
    img.show(out)
    print('Difference:', img.diff(original, out), '%')
    print('Is it letter \'' + img.recognize(img.patterns, out) + '\'?')


if __name__ == '__main__':
    main()
