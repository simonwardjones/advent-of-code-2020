import time

start_time = time.time()


def load_data():
    with open('day_fifteen_data.txt') as fh:
        data = list(map(int, fh.readline().rstrip('\n').split(',')))
    return data


def find_after(after):
    data = load_data()
    last_seen = {number: time for time, number in enumerate(data[:-1])}
    last_number = data[-1]
    for time in range(len(data) - 1, after - 1):
        # print(f'Time: {time}, last_number {last_number}',last_seen)
        if last_number in last_seen:
            diff = time - last_seen[last_number]
            last_seen[last_number] = time
            last_number = diff
        else:
            last_seen[last_number] = time
            last_number = 0
    print(last_number)
    return last_number


def part_one():
    find_after(2020)


def part_two():
    find_after(30000000)


part_one()
part_two()

print("--- %s seconds ---" % (time.time() - start_time))
