import re
import math

f = open('input.txt', 'r')
lines = f.read().split('\n')
instructions = list(lines[0])
instructions = list(map(lambda l: int(l == 'R'), instructions))

data = list(map(lambda line: re.findall(r'[A-Z]+', line), lines[2:]))
dictionary = dict(list(map(lambda line: (line[0], (line[1], line[2])), data)))

# find how many steps till start reaches a Z
def length(s):
	c = 0
	current = s
	l = len(instructions)

	while current[2] != 'Z':
		current = dictionary[current][instructions[c % l]]
		c += 1

	return c

# find LCM of all possible loops
arr = []
for line in data:
	if (line[0][2] == 'A'):
		arr.append(length(line[0]))

print(math.lcm(*arr))