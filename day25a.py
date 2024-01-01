from collections import defaultdict
import heapq

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split(' ') for line in lines]
lines = list(map(lambda line: [line[0][:-1]] + line[1:], lines))
# print(lines)

successors = defaultdict(lambda: [], {})
names = set()

for line in lines:
	names.add(line[0])
	for i in range(1, len(line)):
		successors[line[0]].append(line[i])
		successors[line[i]].append(line[0])
		names.add(line[i])

names = list(names)

# print(successors.items())
# print(names)

def find_path(start, end, successors, banned):
	open_list = [start]
	distances = defaultdict(lambda: float('inf'), {})
	came_from = {}
	distances[start] = 0
	visited = []

	while len(open_list) > 0:
		curr = min(open_list, key=lambda a: distances[a])
		del open_list[open_list.index(curr)]

		if curr in visited:
			continue
		visited.append(curr)

		if curr == end:
			break

		succs = successors[curr]
		for succ in succs:
			if (curr, succ) in banned or (succ, curr) in banned:
				continue

			tentative_dist = distances[curr] + 1
			if tentative_dist < distances[succ]:
				distances[succ] = tentative_dist
				came_from[succ] = curr
				open_list.append(succ)

	if end not in visited:
		return None

	path = []
	current = end
	while current is not None:
		path.insert(0, current)
		current = came_from.get(current, None)

	return path


def same_group(a, b, successors):
	if a == b:
		return True

	banned = []
	for x in range(4):
		path = find_path(a, b, successors, banned)
		# print('path', path)
		if path == None:
			return False
			break
		for i in range(len(path)-1):
			banned.append((path[i], path[i+1]))
		# banned += path[1:-1]

	return True

# print(same_group('bvb', 'xhk', successors))

# group_1 = {names[0]}
# group_2 = set()

# no_need_to_consider = []

# for i, a in enumerate(names):
# 	# print(a, ':')
# 	for j, b in enumerate(names):
# 		print(i, j)
# 		if i <= j:
# 			continue
# 		if same_group(a, b, successors):
# 			if a in group_1 or b in group_1:
# 				group_1.add(a)
# 				group_1.add(b)
# 			# print(b, end = '')
# 			# print(', ', end = '')
# 	# print()

# group_2 = {name for name in names if name not in group_1}

# ans = len(group_1) * len(group_2)
# print(ans)


#speedup ideas:
#precompute pairwise distances then A*


group = [names[0]]
open_list = [names[0]]
visited = [names[0]]

while len(open_list) > 0:
	print(len(open_list))
	curr = open_list[0]
	del open_list[0]

	for succ in successors[curr]:
		if succ in visited:
			continue

		visited.append(succ)
		if same_group(curr, succ, successors):
			open_list.append(succ)
			group.append(succ)


# print(len(group))
ans = len(group) * (len(names) - len(group))
print('ans:', ans)