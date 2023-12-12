# pipe neighbor dictionary
d = {'-': ((-1, 0), (1, 0)), '|': ((0, 1), (0, -1)), 
	 'F': ((0, -1), (1, 0)), 'J': ((-1, 0), (0, 1)), 
	 'L': ((0, 1), (1, 0)), '7': ((-1, 0), (0, -1))}

# yes this messes with state of our input... don't judge
def flood(x, y):
	while lines[y][x] != 'X':
		char = lines[y][x]
		lines[y][x] = 'X'

		# check one way down the pipe
		if (lines[y + d[char][0][1]][x + d[char][0][0]] != 'X'):
				x = x + d[char][0][0]
				y = y + d[char][0][1]
				continue

		# check other way down the pipe
		if (lines[y + d[char][1][1]][x + d[char][1][0]] != 'X'):
				x = x + d[char][1][0]
				y = y + d[char][1][1]

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = list(map(lambda line: list(line), lines))[::-1]
# note the reversal of lines so we can work with "normal" cartesian coords

start_coords = (0, 0)
for y in range(len(lines)):
	if 'S' in lines[y] and lines[y].index('S') != -1:
		start_coords = (lines[y].index('S'), y)

# setting this manually (cringe)
lines[start_coords[1]][start_coords[0]] = '-'
flood(start_coords[0], start_coords[1])

length = 0
for line in lines[::-1]:
	length += line.count('X')
	#print("".join(str(c) for c in line))

ans = int(length/2)
print(ans)
