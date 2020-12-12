from itertools import product


def load_data():
    with open('day_twelve_data.txt') as fh:
        data = [[line[0], int(line[1:])]
                for line in fh.read().splitlines()]
    return data


POLES = [
    [0, [1, 0], 'E'],
    [1, [0, -1], 'S'],
    [2, [-1, 0], 'W'],
    [3, [0, 1], 'N'],
]


def turn(direction, instruction="R", value=90):
    q = int(value / 90)
    return POLES[(direction[0] + q * (1 if instruction == "R" else -1)) % 4]


def step(position, direction, instruction, value):
    if instruction == "F":
        x, y = direction[1]
    else:
        x, y = {p[2]: p[1] for p in POLES}[instruction]
    return (position[0] + (x * value), position[1] + (y * value)), direction


def execute(position, direction, instruction, value):
    if instruction in ["R", "L"]:
        return position, turn(direction, instruction, value)
    elif instruction in ["N", "S", "E", "W", "F"]:
        return step(position, direction, instruction, value)


def part_one():
    data = load_data()
    position, direction = (0, 0), POLES[0]
    for instruction, value in data:
        print(instruction, value)
        position, direction = execute(position, direction, instruction, value)
        print(position, direction)
    print(sum(abs(x) for x in position))


def rotate_way_about_ship(way_position, instruction, value):
    q = int(value / 90)
    x, y = way_position
    return [[x, y], [y, -x], [-x, -y], [-y, x]][(q * (1 if instruction == "R" else -1)) % 4]


def execute_way_point_instruction(ship_position, way_position, instruction, value):
    if instruction in ["N", "S", "E", "W"]:
        way_position, _ = step(way_position, None, instruction, value)
    elif instruction in ["R", "L"]:
        way_position = rotate_way_about_ship(way_position, instruction, value)
    else:
        ship_position = (ship_position[0] + value * way_position[0],
                         ship_position[1] + value * way_position[1])
    return ship_position, way_position


def part_two():
    data = load_data()
    ship_position, way_position = (0, 0), (10, 1)
    for instruction, value in data:
        print(instruction, value)
        ship_position, way_position = execute_way_point_instruction(
            ship_position, way_position, instruction, value)
        print(ship_position, way_position)
    print(sum(abs(x) for x in ship_position))


part_one()
part_two()
