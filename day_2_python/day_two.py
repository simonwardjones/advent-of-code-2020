import pathlib
import logging
from collections import Counter


logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

day_two_data_file = 'day_two_data.txt'
day_two_data_path = pathlib.Path(__file__).parent / day_two_data_file

example = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""


def load_data():
    with open(day_two_data_path, 'r') as fh:
        data = fh.readlines()
    return data


# data = load_data()
# logger.info(f'Loaded data:\n{data}')


def get_parts_one(line):
    user_data = line.strip().split()
    range = [int(x) for x in user_data[0].split('-')]
    letter = user_data[1].strip(':')
    password = user_data[2]
    letter_count = Counter(password)[letter]
    valid = range[0] <= letter_count <= range[1]
    return [range, letter, user_data[2], letter_count, valid]

# print(get_parts('2-9 c: ccccccccc'))

def part_one():
    data = load_data()
    data = [get_parts_one(line) for line in data]
    valid_count = len([line for line in data if line[4]])
    logger.info(valid_count)
    return valid_count

example = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

def get_parts_two(line):
    user_data = line.strip().split()
    range = [int(x) for x in user_data[0].split('-')]
    letter = user_data[1].strip(':')
    password = user_data[2]
    check_letters = [password[index-1] for index in range]
    valid = Counter(check_letters)[letter] == 1
    return [range, letter, user_data[2], check_letters, valid] 


def part_two():
    data = load_data()
    data = [get_parts_two(line) for line in data]
    valid_count = len([line for line in data if line[4]])
    logger.info(valid_count)
    return data




part_one()
part_two()