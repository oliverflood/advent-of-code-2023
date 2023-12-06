import re
import math

class Number:
	def __init__(self, x, y, length, value):
		self.x = x
		self.y = y
		self.length = length
		self.value = value

gear_dict = {}

def gear_append(lines, number):
	# add all numbers to any gears they're next to
	for y in range(max(number.y-1, 0), min(number.y+1, len(lines)-1) +1):
		for x in range(max(number.x-1, 0), min(number.x+number.length, len(lines[0])-1) +1):
			if (lines[y][x] == '*'):
				if (x,y) in gear_dict: 
					gear_dict[(x, y)].append(number.value)
				else: 
					gear_dict[(x, y)] = [number.value]


f = open('input.txt', 'r')
lines = f.read().split('\n')
line_nums_list = [re.findall(r'\d+', line) for line in lines]
numbers_list = []

# fill up our list of Numbers
for y in range(len(lines)):
	prev = 0
	for n in line_nums_list[y]:
		x = lines[y].find(n, prev)
		numbers_list.append(Number(x, y, len(str(n)), int(n)))
		prev = x+1
		# ^forgetting to put a +1 here lost me 2 hours of my life

# add any numbers to their neighboring gears
for Number in numbers_list:
	gear_append(lines, Number)

# grab arrays of gear-related numbers
values = list(gear_dict.values())


ans = sum(list(map(lambda arr: (len(arr) == 2)*math.prod(arr), values)))
print(ans)