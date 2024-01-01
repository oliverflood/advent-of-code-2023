f = open('input.txt', 'r')
lines = f.read().split('\n')
in_len = len(lines)
lines = [list(line) for line in lines]
dirs = [(1,0), (0,1), (-1,0), (0,-1)]
# dirs = [(1,0), (-1,0)]

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def in_bounds(a):
	return a[0] >= 0 and a[0] < len(lines[0]) and a[1] >= 0 and a[1] < len(lines)

middle = (-1, -1)
for y, line in enumerate(lines):
	if middle != (-1, -1):
		break
	try:
		idx = line.index('S')
	except ValueError:
		idx = -1
	if idx != -1:
		middle = (line.index('S'), y)

def p(colors):
	for line in colors:
		for x in line:
			if x == 0:
				print('.', end = '')
			elif x == 1:
				print('*', end = '')
			elif x == 2:
				print('O', end = '')
			else:
				assert(False)
		print()
	print()

def manhattan(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_neighbors(a):
	return [tup_add(a, d) for d in dirs]

def flood_colors(lines, start, start_parity, max_dist):
	open_set = [start]
	colors = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]
	dist_from_start = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]
	colors[start[1]][start[0]] = start_parity

	while len(open_set) > 0:
		curr = open_set[0]
		del open_set[0]

		for neighbor in get_neighbors(curr):
			if not in_bounds(neighbor):
				continue
			if colors[neighbor[1]][neighbor[0]] != 0:
				continue
			if lines[neighbor[1]][neighbor[0]] == '#':
				continue
			# if manhattan(start, neighbor) > max_dist:
			# 	continue
			if dist_from_start[curr[1]][curr[0]] == max_dist:
				continue

			open_set.append(neighbor)
			colors[neighbor[1]][neighbor[0]] = 3-colors[curr[1]][curr[0]]
			dist_from_start[neighbor[1]][neighbor[0]] = dist_from_start[curr[1]][curr[0]] + 1

	# for line in dist_from_start:
	# 	print(line)
	# print('\n\n\n\n\n\n')

	return colors

halfway = (len(lines)-1)//2
starts = [(0,0), (0,len(lines)-1), (len(lines)-1,0), (len(lines)-1,len(lines)-1)]
corner_starts = [(0, halfway), (halfway, 0), (len(lines)-1, halfway), (halfway, len(lines)-1)]

grid = flood_colors(lines, (0,0), 2, 5)

NSTEPS = 26501365
diamond_height = (NSTEPS*2 + 1)//len(lines[0])
corner_parity = 1 if (NSTEPS-(len(lines)-1)//2)%2 == 1 else 2
nibble_parity = 3 - corner_parity
cheese_parity = corner_parity
num_each_nibble = diamond_height//2
num_each_cheese = max(diamond_height//2 - 1, 0)
counting_parity = 1 if NSTEPS%2 == 1 else 2



corner_parity = 1
cheese_parity = 3 - corner_parity
nibble_parity = corner_parity

# corner_parity = 2
# cheese_parity = 3 - corner_parity
# nibble_parity = corner_parity



nibble_colors = []
cheese_colors = []
corner_colors = []

nibble_sum = 0
for n in range(len(starts)):
	nibble_colors = flood_colors(lines, starts[n], nibble_parity, halfway-1)
	nibble_sum += num_each_nibble*sum(row.count(counting_parity) for row in nibble_colors)
	if n == 0:
		p(nibble_colors)
		print('count for nibble', sum(row.count(counting_parity) for row in nibble_colors))

cheese_sum = 0
for n in range(len(starts)):
	cheese_colors = flood_colors(lines, starts[n], cheese_parity, len(lines) + halfway-1)
	cheese_sum += num_each_cheese*sum(row.count(counting_parity) for row in cheese_colors)
	if n == 3:
		p(cheese_colors)
		print('count for cheese', sum(row.count(counting_parity) for row in cheese_colors))


corner_sum = 0
for n in range(len(corner_starts)):
	corner_colors = flood_colors(lines, corner_starts[n], corner_parity, len(lines)-1)
	corner_sum += sum(row.count(counting_parity) for row in corner_colors)
	if n == 2:
		p(corner_colors)
		print('corner count thing: ', sum(row.count(counting_parity) for row in corner_colors))

inner_squares_count = ((diamond_height-2)**2 + 1)//2
# even_sq_count = (inner_squares_count+1)//2  # THIS IS HORRIBLY WRONG
# odd_sq_count = (inner_squares_count-1)//2   # IT TOOK ME SO LONG TO FIGURE OUT THAT THIS IS HORRIBLY WRONG

print(diamond_height)
print(corner_parity)
print(nibble_parity)
print(num_each_nibble)
print(num_each_cheese)
print()

even_sq_count = 1
odd_sq_count = 0
for i in range((diamond_height-1)//2-1):
	if i%2 == 0:
		odd_sq_count += (i+1)*4
	else:
		even_sq_count += (i+1)*4

# even_sq_count = 1
# odd_sq_count = 4

print(even_sq_count)
print(odd_sq_count)
print()


colors = flood_colors(lines, (halfway, halfway), 2, len(lines)*2)
# p(colors)
even_sq_sum = even_sq_count*sum(row.count(counting_parity) for row in colors)

colors = flood_colors(lines, (halfway, halfway), 1, len(lines)*2)
odd_sq_sum = odd_sq_count*sum(row.count(counting_parity) for row in colors)

print(even_sq_sum)
print(odd_sq_sum)
print(nibble_sum)
print(cheese_sum)
print(corner_sum)

ans = even_sq_sum+odd_sq_sum+nibble_sum+cheese_sum+corner_sum
print('ans', ans)



# this code needs some serious refactoring lol