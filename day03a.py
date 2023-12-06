import re

operators = ['+', '$', '#', '@', '-', '=', '&', '%', '/', '*']

class Number:
	def __init__(self, x, y, length, value):
		self.x = x
		self.y = y
		self.length = length
		self.value = value

def symbol_adjacent(lines, number):
	# create set of neighboring cells
	above = lines[max(number.y-1, 0)][max(number.x-1, 0): min(number.x+number.length, len(lines[0])-1) + 1]
	same = lines[number.y][max(number.x-1, 0): min(number.x+number.length, len(lines[0])-1) + 1]
	below = lines[min(number.y+1, len(lines)-1)][max(number.x-1, 0): min(number.x+number.length, len(lines[0])-1) + 1]

	neighbors = set(above) | set(same) | set(below)

	# we're symbol adjacent if we intersect with any operators
	return len(neighbors & set(operators)) > 0


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
		prev = x


ans = sum(list(map(lambda Number: symbol_adjacent(lines, Number)*Number.value, numbers_list)))
print(ans)
