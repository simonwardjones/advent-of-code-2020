from functools import reduce
import re
import time

start_time = time.time()


def load_data():
    with open('day_sixteen_data.txt') as fh:
        data = fh.read()
        rules, your_ticket, nearby_tickets = get_parts(data)
    return rules, your_ticket, nearby_tickets


def get_parts(data):
    rules, your_ticket, nearby_tickets = data.split('\n\n')
    rules = re.findall(r'(\d+)-(\d+)', rules)
    rules = [(int(lower), int(upper)) for lower, upper in rules]
    your_ticket = [int(num) for num in your_ticket.split('\n')[1].split(',')]
    nearby_tickets = [
        [int(num) for num in line.split(',')]
        for line in nearby_tickets.split('\n')[1:]
    ]
    return rules, your_ticket, nearby_tickets


def rules_passed(rules, number):
    return [rule[0] <= number <= rule[1] for rule in rules]


def part_one():
    rules, your_ticket, nearby_tickets = load_data()
    invalid_fields = []
    for ticket in nearby_tickets:
        invalid_fields += [number for number in ticket if not any(
            rules_passed(rules, number))]
    answer = sum(invalid_fields)
    print(answer)


def group_passed(grouped_rules, number):
    return {i
            for i, subrules in enumerate(grouped_rules)
            if any([rule[0] <= number <= rule[1] for rule in subrules])}


def part_two():
    rules, your_ticket, nearby_tickets = load_data()
    grouped_rules = [rules[i:i + 2] for i in range(0, len(rules), 2)]
    potential_tickets = [(ticket, [group_passed(grouped_rules, number) for number in ticket])
                         for ticket in nearby_tickets
                         if not any([not any(rules_passed(rules, number)) for number in ticket])]
    num_rules = len(grouped_rules)

    # for each location, for each ticket show the rules passed at that location
    location_rules_passed = [[pt[1][location_id] for pt in potential_tickets]
                             for location_id in range(num_rules)]
    # summarise for each location the rules that all tickets pass
    location_rules_passed = [list(reduce(set.intersection, location))
                             for location in location_rules_passed]

    lrp = location_rules_passed
    rule_to_id = {}
    while len(rule_to_id.keys()) < num_rules:
        for location, rules in enumerate(lrp):
            if len(rules) == 1:
                remove_rule = rules[0]
                rule_to_id[remove_rule] = location
        lrp = [[rule for rule in rules if rule != remove_rule]
               for rules in lrp]

    ids = [rule_to_id[i] for i in range(6)]
    answer = reduce(lambda x, y: x*y, [your_ticket[id] for id in ids], 1)
    print(answer)
    return answer


part_one()
part_two()

print("--- %s seconds ---" % (time.time() - start_time))
