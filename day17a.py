from collections import defaultdict

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [list(map(int, list(line))) for line in lines]
dirs = [(1,0), (0,1), (-1,0), (0,-1)]

def pr(v):
	for y in range(len(lines)):
		for x in range(len(lines[0])):
			if (x,y) in v:
				print('#', end='')
			else: 
				print('.', end='')
		print()
	print()

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def tup_mul(a, c):
	return tuple(map(lambda elem: elem * c, a))

def in_bounds(a):
	return a[0] >= 0 and a[0] < len(lines[0]) and a[1] >= 0 and a[1] < len(lines)

dir_to_str = {(1,0): 'R', (0,1): 'D', (-1,0): 'L', (0,-1): 'U'}
num_to_dir = {'R' :(1,0), 'D' :(0,1), 'L' :(-1,0), 'U' :(0,-1)}

# node: pos, last_3_dirs
from collections import defaultdict

open_set = {((0,0), ())}

end = (len(lines[0])-1, len(lines)-1)

def end_reached(end, l):
	for item in l:
		if l[0] == end:
			return True
	return False

def h(node):
	return (end[1]-node[0][1]+end[0]-node[0][0])

def concat(tup, elem):
	if tup == ():
		return (elem,)
	if tup[-1] == elem:

		tup = tup + (elem,)
		return tuple(tup[-3:])
	return (elem,)

g_score = defaultdict(lambda: float('inf'), {})
came_from = {}
g_score[((0,0), ())] = 0


c = 0
while len(open_set) > 0:
	curr = min(open_set, key=lambda node: g_score[node]+h(node))

	c += 1
	if c % 1000 == 0:
		print(g_score[curr])
	if curr[0] == end:
		print(g_score[curr])
		print("done")
		break
	
	open_set.remove(curr)

	# look at neighbors
	for d in dirs:
		neighbor_pos = tup_add(d, curr[0]) 
		if not in_bounds(neighbor_pos):
			continue
		if len(curr[1]) >= 3 and d == curr[1][0] and d == curr[1][1] and d == curr[1][2]:
			continue
		if len(curr[1]) >= 1 and d == tup_mul(curr[1][-1], -1):
			continue
		neighbor = (neighbor_pos, concat(curr[1],d))

		tentative_g = g_score[curr] + lines[neighbor_pos[1]][neighbor_pos[0]]

		if tentative_g < g_score[neighbor]:
			g_score[neighbor] = tentative_g
			if neighbor not in open_set:
				# print(neighbor)
				open_set.add(neighbor)
