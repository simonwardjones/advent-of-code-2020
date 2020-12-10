from collections import deque
from collections import Counter


def load_data():
    with open('day_ten_data.txt') as fh:
        data = sorted(list(map(int, fh.readlines())))
    return data


# part 1

def part_one():
    data = load_data()
    count_diffs = Counter(
        [b - a for a, b in zip([0] + data, data+[max(data)+3])])
    answer_1 = count_diffs[1] * count_diffs[3]
    print(answer_1)
    return answer_1

# part 2


def part_two():
    data = load_data()
    a_to_b = {a: [x for x in data if x in range(a+1, a+4)]
              for a in ([0]+data)}

    def get_path_count(current_val, cache={}):
        if current_val in cache:
            return cache[current_val]
        elif current_val == max(data):
            cache[current_val] = 1
        else:
            cache[current_val] = sum([get_path_count(next)
                                      for next in a_to_b[current_val]])
        return cache[current_val]

    answer_2 = get_path_count(0)
    print(answer_2)
    return answer_2


part_one()
part_two()
