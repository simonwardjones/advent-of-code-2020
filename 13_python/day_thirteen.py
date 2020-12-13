import time
start_time = time.time()

from operator import itemgetter


def load_data_one():
    with open('day_thirteen_data.txt') as fh:
        departure = int(fh.readline())
        buses = [int(id) for id in fh.readline().split(',') if id != 'x']
    return departure, buses


def part_one():
    departure, buses = load_data_one()
    next_bus_time = {id: departure + id - (departure % id) for id in buses}
    next_bus = min(next_bus_time.items(), key=itemgetter(1))
    wait = next_bus[1] - departure
    answer = next_bus[0] * wait
    print(answer)
    return answer


def load_data_two():
    with open('day_thirteen_data.txt') as fh:
        departure = int(fh.readline())
        buses = [(i, int(id)) for i, id in enumerate(
            fh.readline().split(',')) if id != 'x']
    return departure, buses


def part_two():
    departure, buses = load_data_two()
    buses = sorted(buses,key=itemgetter(1),reverse=True)
    t = buses[0][1]
    step = 1
    for offset, bus_id in buses:
        while ((t + offset) % bus_id) != 0:
            t += step
        step *= bus_id
    print(t)
    return t

part_one()
part_two()

print("--- %s seconds ---" % (time.time() - start_time))