import re
import time

start_time = time.time()


def load_data():
    with open('day_nineteen_data.txt') as fh:
        raw_rules, raw_messages = fh.read().split('\n\n')
    return raw_rules, raw_messages


raw_rules, raw_messages = load_data()
parsed_rules: dict = {}
raw_rules = [line.split(': ')
             for line in raw_rules.replace('\s', '').split('\n')
             ]
raw_rules = {int(k): v for k, v in raw_rules}


def parse_rules():
    for id, rule in raw_rules.items():
        if id not in parsed_rules:
            rule = parse_rule(id, rule)


def parse_rule(id, rule=None):
    if id in parsed_rules:
        # print(f'Id already processed {id} returning {parsed_rules[id]}')
        rule = parsed_rules[id]
    elif not rule:
        # print(f'No rule given so starting with raw from id {id}: ', raw_rules[id])
        rule = parse_rule(None, raw_rules[id])
    elif '"' in rule:
        # print('ATOM returning', rule.replace('"', ''))
        rule = rule.replace('"', '')
    elif '|' in rule:
        # print("Processing rule with OR")
        rule = '({}|{})'.format(*(parse_rule(None, x)
                                  for x in rule.split(' | ')))
    else:
        # print(f'replacing rule  ids in {rule}')
        rule = re.sub(
            '\d+', lambda x: parse_rule(id=int(x.group(0))), rule).replace(' ', '')
    if id is not None:
        parsed_rules[id] = rule
    return rule


parse_rules()
total = 0
for message in raw_messages.split('\n'):
    if re.match(parsed_rules[0] + '$', message):
        total += 1
print(total)


# part  2
print('#' * 10)

raw_rules, raw_messages = load_data()
parsed_rules: dict = {}
raw_rules = [line.split(': ')
             for line in raw_rules.replace('\s', '').split('\n')]
raw_rules = {int(k): v for k, v in raw_rules if int(k) not in [0, 8, 11]}
# 8 and 11 are only in rule 0 and 8 and 11
parse_rules()

# extras
parsed_rules[8] = f'({parse_rule(42)})+'
parsed_rules[11] = "("+"|".join((parse_rule(42)*n + parse_rule(31)*n)
                                for n in range(1, 7)) + ")"
parsed_rules[0] = parse_rule(None, '8 11')

total = 0
for message in raw_messages.split('\n'):
    if re.match('^'+parsed_rules[0] + '$', message):
        total += 1

print(total)


print("--- %s seconds ---" % (time.time() - start_time))
