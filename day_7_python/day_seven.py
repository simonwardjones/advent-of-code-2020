from collections import defaultdict
import re



def load_data():
    with open('day_seven_data.txt') as fh:
        data = fh.readlines()
    return data

example_bag_rule = \
    'light red bags contain 1 bright white bag, 2 muted yellow bags.'

def parse_bag_rule(bag_rule):
    [first_bag, contains]  = bag_rule.split(' bags contain ')
    included_bag_parts = re.findall(r'(\d) (.*?) bag', contains)
    return [first_bag, included_bag_parts]


def find_bags_containing(bag, parents, allowed_bags):
    for parent in parents[bag]:
        allowed_bags.add(parent)
        find_bags_containing(parent, parents, allowed_bags)
    return allowed_bags

def part_one():
    data = load_data()
    rules = [parse_bag_rule(rule) for rule in data]
    # create parents lookup
    parents = defaultdict(list)
    for parent, children in rules:
        for [count, bag] in children:
            parents[bag].append(parent)
    allowed_bags = find_bags_containing('shiny gold', parents, set())
    print(f'allowed_bags has length {len(allowed_bags)}')


def find_all_bags_inside(bag, children_lookup):
    child_total = 0
    for child_count, child_name in children_lookup[bag]:
        child_total += int(child_count)
        child_total += int(child_count) * find_all_bags_inside(child_name, children_lookup)
    return child_total

def part_two():
    data = load_data()
    children_lookup = dict([parse_bag_rule(rule) for rule in data])
    total = find_all_bags_inside('shiny gold', children_lookup)
    print(f'total bags {total}')

part_one()
part_two()
