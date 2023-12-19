import re
from my_secrets import path

with open(path + 'input19.txt') as f:
    blocks = f.read().split('\n\n')

workflow_lines = blocks[0].split('\n')
part_lines = blocks[1].split('\n')

# idea parse input for interval cutoff points
# add those to a list per component
# so if we come across x>100
# 101 and 100 will give different values for x
# let us store the higher of the two numbers


class workflow_cl():
    def __init__(self, line: str, key: str, rules: list[str]):
        self.line = line
        self.key = key
        self.rules = list()
        for rule in rules:
            self.rules.append(rule_cl(rule))

    def check_part(self, part):
        for rule in self.rules:
            out = rule.check_part(part)
            if out == 'A':
                return 'A'
            elif out == 'R':
                return 'R'
            elif out == 'go_next':
                continue
            else:
                return workflows[out].check_part(part)
        assert False


class workflow_cl_A():
    def check_part(self, part):
        return 'A'


class workflow_cl_R():
    def check_part(self, part):
        return 'R'


class rule_cl():
    def __init__(self, rule):
        self.rule_str = rule
        self.colon_split = rule.split(':')
        self.all_split = re.split('>|<|:', rule)

    def check_part(self, part: dict):
        if len(self.colon_split) == 1:
            return workflows[self.rule_str].check_part(part)
        else:
            greater = re.search(">", self.rule_str)
            less = re.search("<", self.rule_str)
            if greater:
                if part[self.all_split[0]] > int(self.all_split[1]):
                    return workflows[self.all_split[2]].check_part(part)
                else:
                    return 'go_next'
            elif less:
                if part[self.all_split[0]] < int(self.all_split[1]):
                    return workflows[self.all_split[2]].check_part(part)
                else:
                    return 'go_next'
            else:
                print(self.rule_str)
                assert False


def check_part(part):
    out = workflows['in'].check_part(part)
    # if its a good part reject
    # if its a bad part accept
    if out == 'A':
        return True
    elif out == 'R':
        return False
    else:
        print('out', out)
        assert False


global workflows
workflows = {'A': workflow_cl_A(), 'R': workflow_cl_R()}

for line in workflow_lines:
    key = line.split('{')[0]
    rules = line.split('{')[1][:-1].split(',')
    workflows[key] = workflow_cl(line, key, rules)

cutoffs = {'x': {1, 4001},
           'm': {1, 4001},
           'a': {1, 4001},
           's': {1, 4001}}

for line in workflow_lines:
    matches = re.finditer('[0-9]+', line)
    for match in matches:
        number = int(match.group())
        component = line[match.start() - 2]
        symbol = line[match.start() - 1]
        zero_or_one = 0 if symbol == '<' else 1
        cutoffs[component].add(number + zero_or_one)

x_cutoffs = sorted(cutoffs['x'])
m_cutoffs = sorted(cutoffs['m'])
a_cutoffs = sorted(cutoffs['a'])
s_cutoffs = sorted(cutoffs['s'])


ans = 0
print('in about 20 hours you will know the answer')
# :-1 is there since we do not want to do 4001
for index_x, x in enumerate(x_cutoffs[:-1]):
    for index_m, m in enumerate(m_cutoffs[:-1]):
        for index_a, a in enumerate(a_cutoffs[:-1]):
            for index_s, s in enumerate(s_cutoffs[:-1]):
                if check_part({'x': x, 'm': m, 'a': a, 's': s}):
                    weight = (x_cutoffs[index_x + 1] - x) *\
                        (m_cutoffs[index_m + 1] - m) *\
                        (a_cutoffs[index_a + 1] - a) *\
                        (s_cutoffs[index_s + 1] - s)
                    ans += weight
print('ans', ans)
