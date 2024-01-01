from collections import defaultdict

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [list(line.replace('>', '.').replace('v', '.')) for line in lines]
dirs = [(1,0), (0,1), (-1,0), (0,-1)]
end = (lines[-1].index('.'), len(lines)-1)
start = (lines[0].index('.'), 0)

arrow_dir = {'>': (1,0), 'v': (0,1)}

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def tup_mul(a, c):
	return tuple(map(lambda elem: elem * c, a))

def in_bounds(a):
	return a[0] >= 0 and a[0] < len(lines[0]) and a[1] >= 0 and a[1] < len(lines)

def get_neighbors(tup):
	neighbors = []
	for d in dirs:
		neighbor = tup_add(d, tup) 
		if not in_bounds(neighbor):
			continue
		if lines[neighbor[1]][neighbor[0]] == '#':
			continue
		neighbors.append(neighbor)
	return neighbors

def get_directed_neighbors(tup):
	neighbors = []
	for d in dirs:
		neighbor = tup_add(d, tup) 
		if not in_bounds(neighbor):
			continue
		if lines[neighbor[1]][neighbor[0]] == '#':
			continue
		if lines[neighbor[1]][neighbor[0]] != '.' and arrow_dir[lines[neighbor[1]][neighbor[0]]] != d:
			continue
		neighbors.append(neighbor)
	return neighbors

nodes = []
for y in range(len(lines)):
	for x in range(len(lines[0])):
		if lines[y][x] == '.':
			print(len(get_neighbors((x,y))), end='')
			if len(get_neighbors((x,y))) > 2:
				nodes.append((x,y))
		else:
			print(' ', end='')
	print()


def ff_to_successor(nodes, node, neighbor):
	visited = [node, neighbor]
	curr = neighbor
	dist = 1
	while curr not in nodes:
		neighbors = get_neighbors(curr)
		neighbors = list(filter(lambda n: n not in visited, neighbors))
		# print(node, " ", neighbor, " ", neighbors)
		assert(len(neighbors) == 1)
		curr = neighbors[0]
		visited.append(curr)
		dist += 1
	return dist, curr

def generate_successors(nodes, node):
	successors = []
	for neighbor in get_directed_neighbors(node):
		dist, successor = ff_to_successor(nodes, node, neighbor)
		successors.append((successor, dist))
	return successors


for line in lines:
	print(''.join(line))

nodes.append(start)
nodes.append(end)
nodes = tuple(nodes)
print('nodes:', nodes, '\n')

successors = {node: [] for node in nodes}
for node in nodes:
	successors[node] = generate_successors(nodes, node)

# print thing
for node in nodes:
	print(node, " ", successors[node])


# a path is a current node and a visited list
paths = [(start, [start], 0)]
final_path_lengths = []

from collections import defaultdict 
current_max = defaultdict(lambda: 0)


while len(paths) > 0:
	current_path = paths[0]
	# print(current_path)
	# if len(paths) > 5:
	# 	break
	del paths[0]

	if current_path[2]+700 < current_max[current_path[0]]:
		continue
	if current_path[2] > current_max[current_path[0]]:
		current_max[current_path[0]] = current_path[2]

	if current_path[0] == end:
		final_path_lengths.append(current_path[2])
	else:
		for successor in successors[current_path[0]]:
			if successor[0] in current_path[1]:
				continue
			paths.append((successor[0], current_path[1] + [successor[0]], current_path[2]+successor[1]))

print(max(final_path_lengths))
