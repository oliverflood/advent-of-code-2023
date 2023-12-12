import re

f = open('input.txt', 'r')
lines = f.read().split('\n')
instructions = list(lines[0])
instructions = list(map(lambda l: int(l == 'R'), instructions))

data = list(map(lambda line: re.findall(r'[A-Z]+', line), lines[2:]))
dictionary = dict(list(map(lambda line: (line[0], (line[1], line[2])), data)))

# simply go through dict until we hit ZZZ
c = 0
current = 'AAA'
l = len(instructions)
while current != 'ZZZ':
	current = dictionary[current][instructions[c % l]]
	c += 1

print(c)