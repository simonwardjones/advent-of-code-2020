import re
import time
from functools import lru_cache, reduce
from itertools import product

start_time = time.time()


def load_data():
    with open('day_twenty_data.txt') as fh:
        tiles = [Tile(line) for line in fh.read().split('\n\n')]
    return tiles


class Tile:
    def __init__(self, data):
        header, *data = data.split('\n')
        self.id = int(re.findall(r'\d+', header)[0])
        self._data = [[c for c in line] for line in data]
        self.neighbours = {}
        self.loc = None
        self._rotate_by = None  # start of not rotated
        self._flip = None  # start of not flipped
        # print(f'Initiate tile with id: {self.id}')

    @property
    def rotate_by(self):
        return self._rotate_by if self._rotate_by is not None else 0

    @rotate_by.setter
    def rotate_by(self, val):
        if self._rotate_by is not None and self._rotate_by != val:
            raise Exception('Cannot set rotate by more than once',
                            self, self._rotate_by, val)
        self._rotate_by = val

    @property
    def flip(self):
        return self._flip if self._flip is not None else 0

    @flip.setter
    def flip(self, val):
        if self._flip is not None and self._flip != val:
            raise Exception('Cannot set flip by more than once',
                            self, self._flip, val)
        self._flip = val

    def _top(self, rotate_by=None, flip=None):
        return self.get_data(rotate_by, flip)[0]

    def _right(self, rotate_by=None, flip=None):
        return [row[-1] for row in self.get_data(rotate_by, flip)]

    def _bottom(self, rotate_by=None, flip=None):
        return self.get_data(rotate_by, flip)[-1]

    def _left(self, rotate_by=None, flip=None):
        return [row[0] for row in self.get_data(rotate_by, flip)]

    def inner(self):
        return [row[1:9] for row in self.get_data(self.rotate_by, self.flip)[1:9]]

    @lru_cache(maxsize=128)
    def get_data(self, rotate_by=None, flip=None):
        if rotate_by is None:
            rotate_by = self.rotate_by
        if flip is None:
            flip = self.flip
        if rotate_by == 0 and flip == 0:
            return self._data
        elif rotate_by == 1 and flip == 0:
            return [list(row[::-1]) for row in list(zip(*self._data))]
        elif rotate_by == 2 and flip == 0:
            return [row[::-1] for row in self._data[::-1]]
        elif rotate_by == 3 and flip == 0:
            return [list(row) for row in list(zip(*self._data))[::-1]]
        elif rotate_by == 0 and flip == 1:
            return [row for row in self._data[::-1]]
        elif rotate_by == 1 and flip == 1:
            return [list(row[::-1]) for row in list(zip(*self._data))][::-1]
        elif rotate_by == 2 and flip == 1:
            return [row[::-1] for row in self._data[::-1]][::-1]
        elif rotate_by == 3 and flip == 1:
            return [list(row) for row in list(zip(*self._data))]

    def _side_by_id_rotate_flip(self, id, rotate_by=None, flip=None):
        return [self._top, self._right,
                self._bottom, self._left][id](rotate_by, flip)

    def __repr__(self):
        return (f'<Tile{self.id}>\n' +
                '\n'.join(line.__repr__() for line in self._data))

    def to_check(self):
        if self._rotate_by != None:
            return [(self.rotate_by, self.flip)]
        else:
            return product([0, 1, 2, 3], [0, 1])

    def __add__(self, other):
        # print(f'Compare tile {tile.id} to {search_tile.id}')
        for side_id in [0, 1, 2, 3]:
            if side_id in self.neighbours:
                continue
            side = self._side_by_id_rotate_flip(
                side_id, self.rotate_by, self.flip)
            other_side_id = (side_id + 2) % 4
            for rotate_by, flip in other.to_check():
                if other_side_id in other.neighbours:
                    continue
                other_side = other._side_by_id_rotate_flip(
                    other_side_id, rotate_by, flip)
                if side == other_side:
                    # print(f'matched {self.id} to {other.id}')
                    other.rotate_by = rotate_by
                    other.flip = flip
                    self.neighbours[side_id] = other.id
                    other.neighbours[other_side_id] = self.id
                    return True


# example = """Tile 100:
# 12
# 34"""
# tile = Tile(example)
# for rotate_by, flip in product([0, 1, 2, 3], [0, 1]):
#     print(tile.get_data(rotate_by, flip))


def find_neighbours(layer, search):
    if layer:
        next_layer = set()
        for tile_id in layer:
            for search_tile_id in search:
                if tiles_by_id[tile_id] + tiles_by_id[search_tile_id]:
                    next_layer.add(search_tile_id)
        search = [tile.id
                  for tile in tiles
                  if tile.id not in layer and not tile.id in next_layer]
        layer = next_layer
        find_neighbours(layer, search)


tiles = load_data()
tiles_by_id = {tile.id: tile for tile in tiles}
layer = set([tiles[-1].id])
search = set([tile.id for tile in tiles if tile.id not in layer])

find_neighbours(layer, search)

corner_tiles = [tile for tile in tiles if len(tile.neighbours) == 2]
corner_tiles_id = [tile.id for tile in corner_tiles]
answer = reduce(lambda x, y: x*y, corner_tiles_id, 1)
print(answer)

n = int(len(tiles)**0.5)

# one has to be top left ...
tile = [tile
        for tile in corner_tiles
        if 1 in tile.neighbours and 2 in tile.neighbours][0]

tile_grid = [[]]
tile_grid[0].append(tile.id)

for i in range(1, n):
    tile_grid[0].append(
        tiles_by_id[tiles_by_id[tile_grid[0][-1]].neighbours.get(1)].id)

for i in range(n-1):
    tile_grid.append([tiles_by_id[tile_id].neighbours.get(2)
                      for tile_id in tile_grid[-1]])

image = [
    row
    for row_block in [
        [
            [char for sub_row in sub_rows for char in sub_row]
            for sub_rows in zip(*[tiles_by_id[id].inner() for id in row])
        ]
        for row in tile_grid]
    for row in row_block
]


# print("\n".join("".join(row) for row in image))

monster_in = """Tile 1
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
monster: Tile = Tile(monster_in)


h, w = len(monster._data), len(monster._data[0])
N = len(image)
match = 0
for rotate_by, flip in product([0, 1, 2, 3], [0, 1]):
    m_data = monster.get_data(rotate_by, flip)
    h, w = len(m_data), len(m_data[0])
    for row in range(0, N-h+1):
        for col in range(0, N-w+1):
            if all((image[row+i][col+j] == '#' and char == '#') or char != '#'
                   for i, m_row in enumerate(m_data)
                   for j, char in enumerate(m_row)
                   ):
                for i, m_row in enumerate(m_data):
                    for j, char in enumerate(m_row):
                        if char == '#':
                            image[row+i][col+j] = 'O'
                match += 1

print(sum([char == '#' for row in image for char in row]))
# print("\n".join("".join(row) for row in image))

print("--- %s seconds ---" % (time.time() - start_time))
