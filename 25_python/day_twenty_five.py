import time
from collections import defaultdict

start_time = time.time()


def transform(subject_number=7, loop_size=100):
    value = 1
    for _ in range(loop_size):
        value = (value * subject_number) % 20201227
    # print(f'value is {value} with loop size {loop_size}')
    return value


def decrypt(key, value_loop={1: 0}):
    if key in value_loop:
        return value_loop[key]
    subject_number = 7
    value, loop_size = max(value_loop.items(), key=lambda x: x[1])
    while value != key:
        # print(f'value {value}, loop {loop_size}')
        value = (value * subject_number) % 20201227
        loop_size += 1
        value_loop[value] = loop_size
    return loop_size


# sample
card_pulic_key = 5764801
door_pulic_key = 17807724

# my input
card_pulic_key = 6930903
door_pulic_key = 19716708


card_loop_size = decrypt(card_pulic_key)
print(f'Found card_loop_size {card_loop_size}')

door_loop_size = decrypt(door_pulic_key)
print(f'Found door_loop_size {door_loop_size}')

encryption_key = transform(door_pulic_key, card_loop_size)
print(f'encryption_key is {encryption_key}')

print("--- %s seconds ---" % (time.time() - start_time))
