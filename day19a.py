import re
from my_secrets import path

with open(path + 'input19.txt') as f:
    blocks = f.read().split('\n\n')

workflow_lines = blocks[0].split('\n')
part_lines = blocks[1].split('\n')


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

ans = 0
for part_line in part_lines:
    part_line = part_line[1:-1]
    components = part_line.split(',')
    part = dict()
    for component in components:
        part[component[0]] = int(component[2:])

    if check_part(part):
        for key in part:
            ans += part[key]

print(ans)
