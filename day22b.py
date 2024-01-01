from collections import defaultdict
f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split('~') for line in lines]
lines = [[half.split(',') for half in line] for line in lines]
lines = [[[int(pos) for pos in half] for half in line] for line in lines]

# sort by z ascending
lines = sorted(lines, key=lambda brick: max(brick[0][2], brick[1][2]))

# returns set of blocks which make up brick
def calc_block_set(brick):
	brick_blocks = set()
	start = brick[0]
	end = brick[1]

	for x in range(min(start[0], end[0]), max(start[0], end[0])	+1):
		for y in range(min(start[1], end[1]), max(start[1], end[1])+1):
			for z in range(min(start[2], end[2]), max(start[2], end[2])+1):
				brick_blocks.add((x, y, z))

	return brick_blocks

def change_height(block_set, new_z):
	# print('min:', min_height(block_set), 'new_z:', new_z)
	change = min_height(block_set)-new_z
	# if new_z == 4:
	# 	for line in lines[:50]:
	# 		print(line)
	# print(change)
	# print(block_set)
	# print(new_z)
	# print('lowest is now', min_height(block_set) - change + 1)
	assert(change >= 0)
	new_block_set = set(map(lambda block: (block[0], block[1], block[2] - change + 1), block_set))
	return new_block_set

def set_height(block_set, new_z):
	new_block_set = set(map(lambda block: (block[0], block[1], new_z), block_set))
	return new_block_set

def projection(block_set):
	projected_bs = set(map(lambda block: (block[0], block[1]), block_set))
	return projected_bs

def max_height(block_set):
	max_height_block = max(block_set, key=lambda block: block[2])
	return max_height_block[2]

def min_height(block_set):
	min_height_block = min(block_set, key=lambda block: block[2])
	return min_height_block[2]

def removable(i, children, parents):
	if len(children[i]) == 0:
		return True
	for child_index in children[i]:
		if parents[child_index] == [i]:
			return False
	return True

# BFS to find all parents
def all_parents(i, excluded, parents):
	visited = [excluded]
	open_list = [i]
	closed_set = set()

	while len(open_list) > 0:
		curr = open_list[0]
		del open_list[0]

		if curr == excluded:
			exit(4)
			continue

		closed_set.add(curr)

		for parent in parents[curr]:
			if parent not in visited:
				open_list.append(parent)
				visited.append(parent)

	closed_set.remove(i)
	return closed_set

def num_children(i, children):
	visited = []
	open_list = [i]
	closed_set = set()

	while len(open_list) > 0:
		curr = open_list[0]
		del open_list[0]

		closed_set.add(curr)

		for child in children[curr]:
			if child not in visited:
				open_list.append(child)
				visited.append(child)

	closed_set.remove(i)
	return closed_set


memo = {}
def all_children(i, children):
	if i in memo:
		return memo[i]

	if len(children[i]) == 0:
		return set()
	ans = set()
	for child in children[i]:
		ans.add(child)
		# print('adding', child, 'to', i)
		ans = ans.union(all_children(child, children))
	# print('ans for',i,'is',ans)
	memo[i] = ans
	return ans



# block_set is set of blocks for each brick
# ole_block_set = {}
block_set = {}
parents = defaultdict(lambda: [])
children = defaultdict(lambda: [])

already_set = []

for u_index, brick in enumerate(lines):
	block_set[u_index] = calc_block_set(brick)


# block_set = defaultdict(lambda: None)
for u_index, brick in enumerate(lines):
	# upper_brick = ole_block_set[u_index]
	upper_brick = block_set[u_index]

	# print("FOR UPPER BRICK", u_index) 
	# print()
	# print()

	found_z_level = None

	poset = [(max_height(block_set[i_index]), i_index, block_set[i_index]) for i_index in already_set]
	poset = sorted(poset, key=lambda tup: tup[0])


	# if u_index == 1:
	# 	print(poset)
	# 	print('\n\n\n\n\n')
	# assuming lower height bricks are already set as list is sorted
	for x in range(len(poset)-1, -1, -1):
		# if ole_block_set[l_index] == None:
		# 	continue

		# lower_brick = block_set[l_index]
		l_index = poset[x][1]
		lower_brick = poset[x][2]
		# print(already_set)
		if l_index not in already_set:
			continue
		# if max_height(lower_brick) >= min_height(upper_brick):
		# 	continue


		# break when we've found at least one parent and our lower brick can no longer be a parent
		# if found_z_level != None and max_height(lower_brick) < found_z_level:
		# 	break
		
		# print(projection(lower_brick), projection(upper_brick))
		if len(projection(lower_brick).intersection(projection(upper_brick))) > 0:
			if found_z_level != None and found_z_level > max_height(lower_brick):
				break
			found_z_level = max_height(lower_brick)
			children[l_index].append(u_index)
			parents[u_index].append(l_index)

			# if max_height(block_set[l_index]) >= min_height(block_set[u_index]):
			# 	continue
			# print('abt to call change_height:', block_set[l_index])
			block_set[u_index] = change_height(block_set[u_index], max_height(lower_brick))

	if found_z_level == None:
		# print('none womp')
		# print('setting block_set', block_set[u_index],'\nto', end='')
		block_set[u_index] = set_height(block_set[u_index], 1)
		# print(block_set[u_index])
		# print()

	already_set.append(u_index)
	# print("already_set", already_set)


ans = 0
for i in range(len(lines)):
	if not removable(i, children, parents):
		ans += len(num_children(i, children))
		# print(num_children(i, children)[1])

print('ans:',ans)

import sys
sys.setrecursionlimit(3000)
ans = 0
for i in range(len(lines)):
	if not removable(i, children, parents):
		ans += len(all_children(i, children))
		# print(all_children(i, children))

print('ans:',ans)


#119582
#124098
#93364
#69706
#141328
#87710

#76941

roots = set()
for i, block in enumerate(lines):
	# if min_height(block) == 1:
	# 	roots.add(i)
	if parents[i] == []:
		roots.add(i)

# print(roots)

ans = 0
for curr in range(len(lines)):
	# print(curr)

	# if not removable(curr, children, parents):
	for child in all_children(curr, children):
		if len(roots.intersection(all_parents(child, curr, parents))) == 0:
			# print(curr, child, all_children(curr, children), all_parents(child, curr, parents), roots)
			# print('intersection:', roots.intersection(all_parents(child, curr, parents)))
			ans += 1

print('ans:',ans)

# for i in range(len(lines)-1):
# 	assert(i not in children[i])
# 	assert(i not in parents[i])



# for z in range(9, -1, -1):
# 	for x in range(0, 3):
# 		n = True
# 		for brick in range(len(lines)):
# 			if (x, 1, z) in block_set[brick]:
# 				n = False
# 				print(brick, end='')
# 		if n:
# 			print('.', end='')
# 	print()


# for i in range(len(lines)):
# 	print(i, block_set[i])


ans = sum(removable(i, children, parents) for i in range(len(lines)))
print(ans)