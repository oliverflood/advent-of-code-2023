f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split(' ') for line in lines]
lines = list(map(lambda line: [line[0], int(line[1]), line[2]], lines))
dic = {'R': (1,0), 'D': (0,1), 'U': (0,-1), 'L': (-1,0)}
dirs = [(1,0), (0,1), (-1,0), (0,-1)]

def p(a):
	for line in a:
		print(''.join(['.' if c == 0 else '#' for c in line]))
	print()

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def tup_mul(a, c):
	return tuple(map(lambda elem: elem * c, a))

def flood(grid, start):
	open_list = [start]
	while len(open_list) > 0:
		current = open_list[0]

		for d in dirs:
			temp = tup_add(current, d)
			if grid[temp[1]][temp[0]] == 0:
				open_list.append(temp)
				grid[temp[1]][temp[0]] = 1
		del open_list[0]



grid_size = 1000
pos = (int(grid_size/2), int(grid_size/2))
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]



for line in lines:
	for c in range(line[1]+1):
		temp = tup_add(pos, tup_mul(dic[line[0]], c))
		grid[temp[1]][temp[0]] = 1
	pos = tup_add(pos, tup_mul(dic[line[0]], line[1]))

p(grid)
flood(grid, tup_add(pos, (1,1)))
p(grid)

ans = sum(sum(line) for line in grid)
print(ans)