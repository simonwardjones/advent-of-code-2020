import time

start_time = time.time()



def move(cups):
    cup, pickup, rest = cups[0], cups[1:4], cups[4:]
    destination = cup - 1
    if destination == 0:
        destination = 9
    while destination in pickup:
        destination = (destination - 1)
        if destination == 0:
            destination = 9
    dest_idx = rest.index(destination)
    cups = rest[:dest_idx+1] + pickup + rest[dest_idx+1:] + [cup]
    return cups


def part_one():
    cups = list(map(int,'614752839'))
    cups = list(map(int, '389125467'))  # sample

    for round in range(1, 101):
        cups = move(cups)

    one_idx = cups.index(1)
    answer_1 = "".join(map(str, cups[one_idx:] + cups[:one_idx]))[1:]
    print(answer_1)

# part 2 needs a big rethink as the above is too slow!


class Cup:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __repr__(self):
        return f'<{self.val}>'

    def head(self, n):
        if n == 1:
            return str(self.val)
        else:
            return f'{self.val}-{self.next.head(n-1)}'


def move_two(cup, val_to_cup, cup_max):
    pickup = [cup.next, cup.next.next, cup.next.next.next]
    cup.next = pickup[-1].next
    destination_val = cup_max if cup.val == 1 else cup.val - 1
    while destination_val in [cup.val for cup in pickup]:
        destination_val = cup_max if destination_val == 1 else destination_val - 1
    val_to_cup[destination_val].next, pickup[-1].next = pickup[0], val_to_cup[destination_val].next
    return cup.next


def part_two():
    cup_max = 1_000_000
    cups = list(map(int, '614752839')) + list(range(10, cup_max+1))
    cups = list(map(Cup, cups))
    for cup, next_cup in zip(cups, cups[1:]):
        cup.next = next_cup
    cups[-1].next = cups[0]

    val_to_cup = {cup.val: cup for cup in cups}
    cup = cups[0]

    for _ in range(10_000_000):
        cup = move_two(cup, val_to_cup, cup_max)

    print(val_to_cup[1].head(3))
    print(val_to_cup[1].next.val * val_to_cup[1].next.next.val)


part_one()
part_two()
