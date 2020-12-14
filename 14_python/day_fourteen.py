import re
from itertools import product
import time
start_time = time.time()


def load_data():
    with open('day_fourteen_data.txt') as fh:
        data = [get_data(line) for line in fh.readlines()]
    return data


def get_data(line):
    if line[:3] == 'mem':
        return get_mem(line)
    else:
        return get_mask(line)


def get_mask(line):
    return ['mask', line[7:-1]]


def get_mem(line):
    return ['mem', list(map(int, re.findall(r'\d+', line)))]


def part_one():
    data_stream = load_data()
    memory = {}
    mask = None
    for line_type, data in data_stream:
        if line_type == 'mask':
            mask = data
            mask_loc = int(
                ''.join(['1' if x == 'X' else '0' for x in mask]), 2)
            mask_val = int(
                ''.join(['1' if x == '1' else '0' for x in mask]), 2)
        else:
            location, value = data
            memory[location] = ((mask_loc & value) | mask_val)
    answer = sum(memory.values())
    print(answer)
    return answer


def part_two():
    data_stream = load_data()
    memory = {}
    mask = None
    for line_type, data in data_stream:
        if line_type == 'mask':
            mask = data
            not_mask = int(
                ''.join(['1' if x != 'X' else '0' for x in mask]), 2)
            or_mask = int(
                ''.join(['1' if x == '1' else '0' for x in mask]), 2)
            floating_bits = [[2**(35-i), 0]
                             for i, x in enumerate(mask) if x == 'X']
        else:
            location, value = data
            for x in product(*floating_bits):
                memory[(not_mask & (location | or_mask)) | sum(x)] = value
    answer = sum(memory.values())
    print(answer)
    return answer


part_one()
part_two()

print("--- %s seconds ---" % (time.time() - start_time))
