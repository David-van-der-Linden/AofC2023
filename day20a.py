from my_secrets import path
import re

with open(path + 'input20.txt') as f:
    lines = f.read().split('\n')


class Module():
    def __init__(self, line):
        self.type = line[0]
        self.module_name = re.findall('[a-z]+', line)[0]
        self.outputs = re.findall('[a-z]+', line)[1:]
        if self.type == '%':
            self.state = 'off'
        elif self.type == '&':
            self.state = dict()

    def flip_state(self):
        assert self.type == '%'
        if self.state == 'off':
            self.state = 'on'
        elif self.state == 'on':
            self.state = 'off'
        else:
            assert False


class Circuit():
    def __init__(self, lines):
        self.lines = lines
        self.modules = dict()
        for line in lines:
            key = re.findall('[a-z]+', line)[0]
            self.modules[key] = Module(line)

        # finding all inputs to conjunction modules
        for conjunction_module in self.modules.values():
            # conjunction_module = self.modules[conjunction_module_name]
            if conjunction_module.type == '&':
                for module in self.modules.values():
                    if conjunction_module.module_name in module.outputs:
                        # add input
                        conjunction_module.state[module.module_name] = 'low'

    def process_button_press(self):
        module_queue = self.modules['broadcaster'].outputs
        queue = [('low', module_name, 'broadcaster') for module_name in module_queue]
        low_pulses_sent = 1
        high_pulses_sent = 0
        while len(queue) > 0:
            task = queue.pop(0)
            pulse_strength = task[0]
            module_name = task[1]
            received_from = task[2]

            # print(received_from, pulse_strength, '->', module_name)

            if pulse_strength == 'low':
                low_pulses_sent += 1
            elif pulse_strength == 'high':
                high_pulses_sent += 1
            else:
                assert False
            
            if module_name in self.modules:
                module = self.modules[module_name]
            else:
                continue

            if module.type == '%':
                if pulse_strength == 'high':
                    pass  # do nothing
                elif pulse_strength == 'low':
                    new_pulse_strength = 'high' if module.state == 'off' else 'low'
                    # print(module.state == 'on')
                    # print('new_pulse_strength', new_pulse_strength)
                    # print('module.module_name', module.module_name)
                    # print('module.state', module.state)
                    for output in module.outputs:
                        queue.append((new_pulse_strength, output, module_name))
                    module.flip_state()
                    # print('state was flipped')
                    # print('module.state', module.state)
                else:
                    assert False

            elif module.type == '&':
                module.state[received_from] = pulse_strength
                # are all entry's the same and high?
                all_high = len(set(module.state.values())) == 1 and \
                    list(module.state.values())[0] == 'high'
                new_pulse_strength = 'low' if all_high else 'high'
                for output in module.outputs:
                    queue.append((new_pulse_strength, output, module_name))
        return (low_pulses_sent, high_pulses_sent)


my_s = Circuit(lines)
lps, hps = 0, 0
for _ in range(1000):
    tup = my_s.process_button_press()
    lps += tup[0]
    hps += tup[1]
ans = lps * hps
print('ans', ans)
# assert ans == 11687500