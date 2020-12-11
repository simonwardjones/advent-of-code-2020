from itertools import product


def load_data():
    with open('day_eleven_data.txt') as fh:
        data = [[convert_string(code) for code in line]
                for line in fh.read().splitlines()]
    return data


CODE_TO_NUMBER = {
    'L': 0,
    '#': 1,
    '.': 0,
}


def convert_string(code):
    return code, CODE_TO_NUMBER[code]


# part 1

def update(data):
    rows, cols = len(data), len(data[0])
    update = [[0 for _ in range(cols)] for _ in range(rows)]
    for r_id, c_id in product(range(rows), range(cols)):
        neighbours = sum([int(col[1]) for row in data[max(r_id-1, 0):r_id+2]
                          for col in row[max(c_id-1, 0):c_id+2]]) - (
            data[r_id][c_id][1])
        if data[r_id][c_id][0] == 'L' and neighbours == 0:
            update[r_id][c_id] = ['#', 1]
        elif data[r_id][c_id][0] == '#' and neighbours > 3:
            update[r_id][c_id] = ['L', 0]
        else:
            update[r_id][c_id] = data[r_id][c_id]
    stable = all(update[r_id][c_id][0] == data[r_id][c_id][0]
                 for r_id, c_id in product(range(rows), range(cols)))
    return update, stable


def display(data):
    for line in [[v[0] for v in line] for line in data]:
        print(line)
    print()


def part_one():
    data = load_data()
    rows, cols = len(data), len(data[0])
    stable = False
    while not stable:
        data, stable = update(data)
    answer = sum(data[r_id][c_id][0] == '#'
                 for r_id, c_id in product(range(rows), range(cols)))
    print(answer)
    return answer


def update_two(data):
    rows, cols = len(data), len(data[0])
    update = [[[] for _ in range(cols)] for _ in range(rows)]
    for r_id, c_id in product(range(rows), range(cols)):
        if data[r_id][c_id][0] == '.':
            update[r_id][c_id] = ['.', 0]
            continue
        neighbours = [
            occupied_in_direction(r_id, c_id, r_step, c_step, data)
            for r_step, c_step in [
                # adjacents
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                # diagonals
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]
        ]
        neighbours = sum(neighbours)
        if data[r_id][c_id][0] == 'L' and neighbours == 0:
            update[r_id][c_id] = ['#', 1]
        elif data[r_id][c_id][0] == '#' and neighbours > 4:
            update[r_id][c_id] = ['L', 0]
        else:
            update[r_id][c_id] = data[r_id][c_id]
    stable = all(update[r_id][c_id][0] == data[r_id][c_id][0]
                 for r_id, c_id in product(range(rows), range(cols)))
    return update, stable


def occupied_in_direction(r_id, c_id, r_step, c_step, data):
    rows, cols = len(data), len(data[0])
    r_id += r_step
    c_id += c_step
    while r_id in range(rows) and c_id in range(cols):
        if data[r_id][c_id][0] == '#':
            return 1
        if data[r_id][c_id][0] == 'L':
            return 0
        r_id += r_step
        c_id += c_step
    return 0

# part 2


def part_two():
    data = load_data()
    rows, cols = len(data), len(data[0])
    stable = False
    while not stable:
        data, stable = update_two(data)
    answer = sum(data[r_id][c_id][0] == '#'
                 for r_id, c_id in product(range(rows), range(cols)))
    print(answer)
    return answer


part_one()
part_two()