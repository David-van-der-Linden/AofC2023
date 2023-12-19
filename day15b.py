from my_secrets import path
import re
from collections import OrderedDict

with open(path + 'input15.txt') as f:
    steps = f.read().split(',')

# idea keep a dictionary containing the nonempty boxes
# inside call that dictionary with the box_nr to a box
# in each box store the labels and the focal_length of
# the lenses in the form of an ordered dictionary


def get_hash(step):
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value = current_value * 17
        current_value = current_value % 256
    return current_value


boxes = {}

for step in steps:
    operation = re.findall('=|-', step)
    split_step = re.split('=|-', step)
    label = split_step[0]
    box_nr = get_hash(label)
    boxes.setdefault(box_nr, OrderedDict())
    if operation == ['=']:
        focal_length = int(split_step[1])
        boxes[box_nr][label] = focal_length
    elif operation == ['-']:
        if label in boxes[box_nr]:
            boxes[box_nr].pop(label)
    else:
        assert False

ans = 0
for box_nr in boxes:
    for label in boxes[box_nr]:
        ans += (box_nr + 1) * \
            (list(boxes[box_nr].keys()).index(label) + 1) * \
            boxes[box_nr][label]

print(ans)
