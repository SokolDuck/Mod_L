import numpy as np
import matplotlib.pyplot as plt

from src.LR1.constants import COUNT, X0, A, M, HISTOGRAM_COUNT
from src.LR1.random_lemera import LemerRandomGenerator


def generate_random_sequence(count=COUNT, x0=X0, a=A, m=M):
    lem_rand_obj = LemerRandomGenerator(x0, a, m)
    return [lem_rand_obj.get_next_random() for _ in range(count)]


random_num = generate_random_sequence()


def build_hist(random_seq: list, hist_count=HISTOGRAM_COUNT):
    plt.hist(random_seq, hist_count)
    plt.show()


def calculate_mat_var(random_seq: list):
    arr = np.array(random_seq)

    print(f'random sequence\n{arr}')
    print(f'Mean = {arr.mean()}')
    print(f'Var = {arr.var()}')
    print(f'Std = {arr.std()}')


def check_for(random_seq: list):
    N = len(random_seq)
    if N % 2 != 0:
        random_seq.append(random_seq[-1])
    list_of_pairs = [(random_seq[i], random_seq[i + 1]) for i in range(0, N, 2)]
    K = len(list(filter(lambda x: x[0] ** 2 + x[1] ** 2 < 1, list_of_pairs)))

    print(f'K = {K}')
    print(f'2K / N = {2 * K / N}')
    print(f'pi/4 = {np.pi / 4}')


if __name__ == '__main__':

    build_hist(random_num)
    calculate_mat_var(random_num)
    check_for(random_num)

    plt.plot(range(len(random_num)), random_num, 'bo')
    plt.show()

    obj = LemerRandomGenerator(X0, A, M)
    p, aper = obj.calculate_period()
    print(f'Period P = {p}, {aper}')

    # fix_1 = obj.get_next_random()
    # fix_2 = obj.get_next_random()
    #
    # for _ in range(p - 1):
    #     obj.get_next_random()
    #
    # check_1 = obj.get_next_random()
    # check_2 = obj. get_next_random()
    #
    # print(f'fix_1 ({fix_1}) == check_1 ({check_1}) {fix_1 == check_1}')
    # print(f'fix_2 ({fix_2}) == check_2 ({check_2}) {fix_2 == check_2}')


