f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = list(map(lambda line: list(line), lines))

x_indexes = []
y_indexes = []
galaxies = []

def dist(gal_1, gal_2):
	x1, y1 = gal_1
	x2, y2 = gal_2

	extra_space = sum([1 if (x > x1 and x < x2) or (x < x1 and x > x2) else 0 for x in x_indexes])
	extra_space += sum([1 if (y > y1 and y < y2) or (y < y1 and y > y2) else 0 for y in y_indexes])

	return abs(x1 - x2) + abs(y1 - y2) + extra_space

# add indexes where universe expands for y
for y, line in enumerate(lines):
	if line == ['.']*len(line):
		y_indexes.append(y)

# add indexes where universe expands for x
for x in range(len(lines[0])):
	no_gals = True
	for y in range(len(lines)):
		if (lines[y][x] == '#'):
			no_gals = False
	if no_gals:
		x_indexes.append(x)

# add galaxies 
for y in range(len(lines)):
	for x in range(len(lines[y])):
		if lines[y][x] == '#':
			galaxies.append((x, y))

ans = 0
for i in range(len(galaxies)):
	for j in range(i+1, len(galaxies)):
		ans += dist(galaxies[i], galaxies[j])

print(ans)