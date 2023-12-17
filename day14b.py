from copy import deepcopy
f = open('input.txt', 'r')
lines = list(map(list, f.read().split('\n')))
# note: program could use refactoring :')

# get the weight total of a board
def total(m):
	ans = 0
	for y in range(len(m)):
		ans += sum(len(m)-y if c == 'O' else 0 for c in m[y])
	return ans

# print a matrix (very helpful)
def p(m):
	for y in range(len(m)):
		print(str(m[y]))
	print()

# rotate clockwise (prints as counter-clockwise)
def rotate(m):
	return [[m[len(m[0])-1-x][y] for x in range(len(m[0]))] for y in range(len(m))]

# move all O's in a column north
def move_column(m, x):
	ans = 0
	wallpos = -1
	new_y_vals = []
	new_m = m

	for y in range(len(m)):
		if m[y][x] == 'O':
			wallpos += 1
			new_m[y][x] = '.'
			new_m[wallpos][x] = 'O'
			
		if m[y][x] == '#':
			wallpos = y

	return new_m

# tilt a whole board north
def tilt(m):
	for x in range(len(m[0])):
		m = move_column(m, x)
	return m

# complete a cycle of four tilts and rotations
def cycle(m):
	return rotate(tilt(rotate(tilt(rotate(tilt(rotate(tilt(m))))))))


# states have no memory, so once we find a repeat we can mod out a lot of computation

c = 0 # c identifies cycle c
done = [] # done lists all board states seen so far

while True:	
	prev = deepcopy(lines) # <- I believe we must deepcopy here
	done.append(prev)
	lines = cycle(lines)
	c += 1

	# we can stop after reaching a billion computed cycles
	if c == 1000000000:
		break

	# mod out computations
	if lines in done:
		c = 1000000000 - ((1000000000-c) % (len(done) - done.index(lines)))

final_board = cycle(done[len(done)-1])
# p(final_board)
print(total(final_board))