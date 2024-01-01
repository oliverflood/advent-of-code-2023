from collections import defaultdict
f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split('~') for line in lines]
lines = [[half.split(',') for half in line] for line in lines]
lines = [[[int(pos) for pos in half] for half in line] for line in lines]

# sort by z ascending
lines = sorted(lines, key=lambda brick: min(brick[0][2], brick[1][2]))

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
	m = min_height(block_set)
	new_block_set = set(map(lambda block: (block[0], block[1], block[2]-(m-new_z)), block_set))
	return new_block_set

# def set_height(block_set, new_z):
# 	new_block_set = set(map(lambda block: (block[0], block[1], new_z), block_set))
# 	return new_block_set

def projection(block_set):
	projected_bs = set(map(lambda block: (block[0], block[1]), block_set))
	return projected_bs

def max_height(block_set):
	max_height_block = max(block_set, key=lambda block: block[2])
	return max_height_block[2]

def min_height(block_set):
	return min(block_set, key=lambda block: block[2])[2]

def is_removable(children, parents, i):
	if len(children[i]) == 0:
		return True
	for child_index in children[i]:
		if parents[child_index] == [i]:
			return False
	return True


# block_set is set of blocks for each brick
block_set = {}
parents = defaultdict(lambda: [])
children = defaultdict(lambda: [])

for u_index, brick in enumerate(lines):
	block_set[u_index] = calc_block_set(brick)


for u_index, brick in enumerate(lines):
	upper_brick = block_set[u_index]

	# found_z_level = None

	poset = [(max_height(block_set[i_index]), i_index, block_set[i_index]) for i_index in range(len(lines))]
	poset = sorted(poset, key=lambda tup: tup[0])

	print(u_index, poset)

	done = False
	for height in range(min_height(upper_brick)-1, 0, -1):
		if done:
			break
		for x in range(len(list(filter(lambda tup: tup[0] == height, poset)))):

			l_index = poset[x][1]
			lower_brick = poset[x][2]

			# break when we've found at least one parent and our lower brick can no longer be a parent
			# if found_z_level != None and max_height(lower_brick) < found_z_level:
			# 	break
			
			if len(projection(lower_brick).intersection(projection(upper_brick))) > 0:
				# found_z_level = max_height(lower_brick)
				children[l_index].append(u_index)
				parents[u_index].append(l_index)
				block_set[u_index] = change_height(block_set[u_index], max_height(lower_brick))
				done = True



	# for x in range(len(poset)):

	# 	l_index = poset[x][1]
	# 	lower_brick = poset[x][2]

	# 	if max_height(lower_brick) + 1 != min_height(upper_brick):
	# 		continue


	# 	# break when we've found at least one parent and our lower brick can no longer be a parent
	# 	# if found_z_level != None and max_height(lower_brick) < found_z_level:
	# 	# 	break
		
	# 	if len(projection(lower_brick).intersection(projection(upper_brick))) > 0:
	# 		# found_z_level = max_height(lower_brick)
	# 		children[l_index].append(u_index)
	# 		parents[u_index].append(l_index)
	# 		block_set[u_index] = change_height(block_set[u_index], max_height(lower_brick) + 1)



ans = [is_removable(children, parents, i) for i in range(len(lines))]
print(ans)

print(children.items())
print(parents.items())

for z in range(9, -1, -1):
	for x in range(0, 3):
		n = True
		for brick in range(len(lines)):
			if (x, 1, z) in block_set[brick]:
				n = False
				print(brick, end='')
		if n:
			print('.', end='')
	print()