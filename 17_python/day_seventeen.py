import time
import numpy as np
from itertools import product

start_time = time.time()


def load_data():
    with open('day_seventeen_data.txt') as fh:
        return [[1 if cube == '#' else 0 for cube in line.rstrip()]
                for line in fh.readlines()]


def initialise_pocket_dimension(init_data, n_rounds=6, n_dim=3):
    len_data = len(init_data)
    init_data = np.array(init_data)
    final_shape = len_data + (2 * n_rounds)
    center_id = int((final_shape - 1)/2)
    pocket_dimension = np.zeros((final_shape,) * n_dim)
    mask = tuple(center_id for _ in range(n_dim-2)) + \
        ((slice(n_rounds, n_rounds + len_data),) * 2)
    pocket_dimension[mask] = init_data.reshape(len_data, len_data)
    return pocket_dimension, final_shape


def get_sum_after(n_dim=3, n_rounds=6):
    init_data = load_data()
    pocket_dimension, final_shape = initialise_pocket_dimension(
        init_data, n_rounds, n_dim)
    for round in range(n_rounds):
        pocket_dimension_after_round = np.zeros((final_shape,) * n_dim)
        for loc in product(*((range(final_shape),) * n_dim)):
            slices = tuple(slice(max(0, dim-1), dim+2) for dim in loc)
            neighbours = pocket_dimension[slices].sum()
            if pocket_dimension[loc] == 1:
                if neighbours in [3, 4]:
                    pocket_dimension_after_round[loc] = 1
                else:
                    pocket_dimension_after_round[loc] = 0
            if pocket_dimension[loc] == 0:
                if neighbours == 3:
                    pocket_dimension_after_round[loc] = 1
                else:
                    pocket_dimension_after_round[loc] = 0
        pocket_dimension = pocket_dimension_after_round
    print(pocket_dimension_after_round.sum())


get_sum_after()
get_sum_after(4)

print("--- %s seconds ---" % (time.time() - start_time))
