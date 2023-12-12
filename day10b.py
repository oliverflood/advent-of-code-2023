# pipe neighbor dictionary
d = {'-': ((-1, 0), (1, 0)), '|': ((0, 1), (0, -1)), 
	 'F': ((0, -1), (1, 0)), 'J': ((-1, 0), (0, 1)), 
	 'L': ((0, 1), (1, 0)), '7': ((-1, 0), (0, -1))}

# doesn't mess with state of input
def flood(x, y):
	while visited[y][x] == False:
		char = lines[y][x]
		visited[y][x] = True

		# check one way down the pipe
		if (visited[y + d[char][0][1]][x + d[char][0][0]] == False):
				x = x + d[char][0][0]
				y = y + d[char][0][1]
				continue

		# check other way down the pipe
		if (visited[y + d[char][1][1]][x + d[char][1][0]] == False):
				x = x + d[char][1][0]
				y = y + d[char][1][1]

def vertical_parity(x, y, lines):
	p = 0
	for i in range(y):
		if lines[i][x] in ['F', 'J']:
			p += 0.5
		if lines[i][x] in ['7', 'L']:
			p -= 0.5
		if lines[i][x] == '-':
			p += 1
	return int(p) % 2

def horizontal_parity(x, y, lines):
	p = 0
	for i in range(x):
		if lines[y][i] in ['F', 'J']:
			p += 0.5
		if lines[y][i] in ['L', '7']:
			p -= 0.5
		if lines[y][i] == '|':
			p += 1
	return int(p) % 2

# many thanks to my knot theory class
def in_loop(x, y, lines):
	return vertical_parity(x, y, lines) + horizontal_parity(x, y, lines) == 2


f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = list(map(lambda line: list(line), lines))[::-1]
# note the reversal of lines so we can work with "normal" cartesian coords
visited = list(map(lambda line: [0]*len(line), lines))

start_coords = (0, 0)
for y in range(len(lines)):
	if 'S' in lines[y] and lines[y].index('S') != -1:
		start_coords = (lines[y].index('S'), y)

# setting this manually (cringe)
lines[start_coords[1]][start_coords[0]] = '-' # <- MANUALLY SET LOL
flood(start_coords[0], start_coords[1])

# get rid of unnecessary lines (this changes our original input!!)
lines = [[lines[y][x] if visited[y][x] == True else '.' for x in range(len(lines[y]))] for y in range(len(lines))]

# check crossing numbers
ans = 0
for y in range(len(lines)):
	for x in range(len(lines[y])):
		if lines[y][x] == '.' and in_loop(x, y, lines):
			ans += 1
print(ans)
