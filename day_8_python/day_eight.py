import re
from collections import defaultdict


def load_data():
    with open('day_eight_data.txt') as fh:
        data = fh.readlines()
    pairs = [step.replace("\n", "").split(" ") for step in data]
    return [(name, int(value)) for name, value in pairs]


class Programme:
    def __init__(self, steps):
        self.steps = steps
        self.vistied_nop_jmp = set()
        self._reset()
        self.search_index = None

    def _reset(self):
        self.accumulator = 0
        self.visited = set()
        self.index = 0

    def run(self, record=False):
        self._reset()
        while self.is_valid_index():
            self.operate(record)
        return self.accumulator

    def is_valid_index(self):
        if self.index == len(self.steps):
            print(
                f'COMPLETED, search_index={self.search_index} '
                f'Accumulator value {self.accumulator}')
            self.bug_index = self.search_index
            return False
        elif self.index not in self.visited:
            return True
        else:
            return False

    def operate(self, record):
        name, value = self.steps[self.index]
        if self.search_index == self.index:
            name = self._swap_name(name)
        self.visited.add(self.index)
        if name == 'nop':
            if record:
                self.vistied_nop_jmp.add(self.index)
            self.index += 1
        elif name == 'acc':
            self.index += 1
            self.accumulator += value
        elif name == 'jmp':
            if record:
                self.vistied_nop_jmp.add(self.index)
            self.index += value

    def _swap_name(self, name):
        if name == "nop":
            return "jmp"
        elif name == "jmp":
            return "nop"
        return name

    def find_bug(self):
        self.run(record=True)
        for index in self.vistied_nop_jmp:
            # print(f'Checking index {index}')
            self.search_index = index
            self.run()
        self.search_index = None

data = load_data()
programme = Programme(steps=data)

print(programme.run(record=True))
programme.find_bug()

