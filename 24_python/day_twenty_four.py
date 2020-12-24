import time
from collections import defaultdict

start_time = time.time()


def load_data():
    with open('day_twenty_four_data.txt') as fh:
        data = fh.read().split('\n')
        return data


class Tile:
    black_tiles = set()

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Tile(self.x + other.x, self.y + other.y)

    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def colour(self):
        return 1 if self.coordinates in self.black_tiles else 0

    def flip(self):
        if self.coordinates in self.black_tiles:
            self.black_tiles.remove(self.coordinates)
        else:
            self.black_tiles.add(self.coordinates)

    @property
    def neighbours(self):
        for step in direction_steps.values():
            yield (self + step).coordinates

    def __repr__(self):
        return f'({self.x},{self.y})'


direction_steps = {
    'e': Tile(1, 0),
    'se': Tile(0, -1),
    'sw': Tile(-1, -1),
    'w': Tile(-1, 0),
    'nw': Tile(0, 1),
    'ne': Tile(1, 1),
}


def get_tile(line: str):
    current_tile = Tile(0, 0)
    while line:
        for direction, step in direction_steps.items():
            if line.startswith(direction):
                # print(f'Steping in dir {direction}')
                current_tile += step
                line = line[len(direction):]
    return current_tile


def part_one():
    data = load_data()
    tiles = [get_tile(tile_directions)
             for tile_directions in data]
    black_tiles = set()
    for tile in tiles:
        tile.flip()
    answer = len(Tile.black_tiles)
    print(answer)


part_one()


def step_day():
    # print(f'black tiles {Tile.black_tiles}')

    coord_to_check = set()
    for coord in Tile.black_tiles:
        coord_to_check.add(coord)
        tile = Tile(*coord)
        for n_coord in tile.neighbours:
            coord_to_check.add(n_coord)
    # print(f'Coordinates to check (with a black neighbour or black)',coord_to_check)

    tiles_to_flip = []
    for coord in coord_to_check:
        tile = Tile(*coord)
        black_neighbours = sum(
            Tile(*n_tile).colour for n_tile in tile.neighbours)
        if tile.colour == 1 and black_neighbours not in [1, 2]:
            tiles_to_flip.append(tile)
        elif tile.colour == 0 and black_neighbours == 2:
            tiles_to_flip.append(tile)
    # print(tiles_to_flip)

    for tile in tiles_to_flip:
        tile.flip()


for _ in range(100):
    step_day()

print(len(Tile.black_tiles))


print("--- %s seconds ---" % (time.time() - start_time))
