from collections import deque


def load_data():
    with open('day_nine_data.txt') as fh:
        data = list(map(int, fh.readlines()))
    return data


def part_one():
    data = load_data()


def update_store(store, next_number):
    store.popleft()  # remove old list
    for item in store:
        item[1].append(item[0] + next_number)
    store.append([next_number, []])
    return store


def check_valid(store, next_number):
    for item in store:
        for value in item[1]:
            # print('checking',next_number, value)
            if next_number == value:
                return True
    print(f'Fail {next_number}')
    return False


def part_one():
    data = load_data()
    # the store has a row for each n preceding rows containing a pair
    # the first is the number the second a list of all valid_numbers
    # made with that number
    preamble_size = 25
    preamble = data[:preamble_size]
    store = deque([[d, [d + a for a in preamble[i+1:]]]
                    for i, d in enumerate(preamble)])
    index = preamble_size
    while index < len(data):
        # print(f'checking index {index}')
        next_number = data[index]
        number_valid = check_valid(store, next_number)
        if not number_valid:
            return ( next_number, store, index)
        store = update_store(store, next_number)
        index += 1




def part_two(next_number,index):
    data = load_data()
    search_data = data[:index]
    search_data.reverse()
    max_stream = len(search_data)
    for i in range(max_stream):
        for j in range(1,max_stream - i):
            # print(i, search_data[i], search_data[i:i+j])
            if sum(search_data[i:i+j]) == next_number:
                print(max(search_data[i:i+j]) + min(search_data[i:i+j]))
                return max(search_data[i:i+j]) + min(search_data[i:i+j])
            elif sum(search_data[i:i+j]) > next_number:
                break

next_number, store , index = part_one()
part_two_sum = part_two(next_number,index)