f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [list(line) for line in lines]
dirs = [(1,0), (0,1), (-1,0), (0,-1)]

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def in_bounds(a):
	return a[0] >= 0 and a[0] < len(lines[0]) and a[1] >= 0 and a[1] < len(lines)

start = (-1, -1)
for y, line in enumerate(lines):
	if start != (-1, -1):
		break
	try:
		idx = line.index('S')
	except ValueError:
		idx = -1
	if idx != -1:
		start = (line.index('S'), y)

# here colors acts as a visited list
def ff_increment(lines, colors, open_list, COND, COND_2):
	new_open_list = []
	while len(open_list) > 0:
		curr = open_list[0]
		del open_list[0]

		for d in dirs:
			neighbor = tup_add(d, curr)

			if COND:
				if d == (0,-1) or d == (-1,0):
					continue
				left = tup_add((-1,0), neighbor)
				right = tup_add((0,-1), neighbor)
				if COND_2 and (in_bounds(left) and in_bounds(right)) and (colors[left[1]][left[0]] == 0 or colors[right[1]][right[0]] == 0):
					continue

			if not in_bounds(neighbor):
				continue
			if lines[neighbor[1]][neighbor[0]] == '#':
				continue
			if colors[neighbor[1]][neighbor[0]] != 0:
				continue

			# we pass all conditions ->
			assert(colors[curr[1]][curr[0]] == 1 or colors[curr[1]][curr[0]] == 2)
			colors[neighbor[1]][neighbor[0]] = 3 - colors[curr[1]][curr[0]]
			new_open_list.append(neighbor)

	return colors, new_open_list




colors = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]
colors[start[1]][start[0]] = 2
open_list = [start]

NUM_STEPS = 64
for step in range(NUM_STEPS):
	colors, open_list = ff_increment(lines, colors, open_list, False, False)

ans = sum(row.count(2) for row in colors)
print(ans)