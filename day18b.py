from functools import reduce 
f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split(' ') for line in lines]

# could just be one dic but I feel this is clearer
last_char_dic = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
dic = {'R': (1,0), 'D': (0,1), 'U': (0,-1), 'L': (-1,0)}
dirs = [(1,0), (0,1), (-1,0), (0,-1)]

correct_rects = []

def p(a):
	for line in a:
		print(''.join(['.' if c == 0 else '#' for c in line]))
	print()

def char_val(c):
	if c.isdigit():
		return ord(c)-48
	return ord(c)-87

def hex_to_int(h):
	h = h[::-1]
	ans = 0
	for i, c in enumerate(list(h)):
		ans += 16**i * char_val(c)
	return ans

def area(ra, rb):
	return (ra[1]-ra[0])*(rb[1]-rb[0])


# can assume x_bars is sorted by y heights
def contribution(rect, x_bars, y_bars):
	assert(isinstance(rect[0][0], int))
	assert(isinstance(x_bars[0][0][0], int))
	# print(rect, "  ", sum(1 if rect[0][0] >= x_bar[0][0] and rect[0][1] <= x_bar[0][1] and rect[1][0] >= x_bar[1] else 0 for x_bar in x_bars) or (rect[1][0] == x_bar[1] for x_bar in x_bars))
	# if (sum(1 if rect[0][0] >= x_bar[0][0] and rect[0][1] <= x_bar[0][1] and rect[1][0] >= x_bar[1] else 0 for x_bar in x_bars)%2 == 1) or (rect[1][0] in list(map(lambda x_bar: x_bar[1], x_bars))):
	# 	# print(rect)
	# 	correct_rects.append(rect)

	discriminator = 0
	discriminator2 = 0
	for x_bar in x_bars:
		if rect[0][0] >= x_bar[0][0] and rect[0][1] < x_bar[0][1] and rect[1][0] >= x_bar[1]:
			discriminator += 1

		# if rect[0][0] >= x_bar[0][0] and rect[0][1] <= x_bar[0][1] and rect[1][0] == x_bar[1]:
		# 	correct_rects.append(rect)
		# 	# print(rect, 'on', x_bar)
		# 	return area(rect[0], rect[1])

		#### if (rect[0][0] >= x_bar[0][0] and rect[0][1] == x_bar[0][1] and rect[1][0] >= x_bar[1]):

	for y_bar in y_bars:
		if rect[1][0] >= y_bar[0][0] and rect[1][1] < y_bar[0][1] and rect[0][1]-1 >= y_bar[1]:
			discriminator2 += 1

		# if rect[1][0] >= y_bar[0][0] and rect[1][1] <= y_bar[0][1] and rect[0][1]-1 == y_bar[1]:
		# 	correct_rects.append(rect)
		# 	# print(rect, 'on', x_bar)
		# 	return area(rect[0], rect[1])

	# print(rect, " ", discriminator)

	if discriminator % 2 == 1:
		correct_rects.append(rect)
		return area(rect[0], rect[1])

	if discriminator2 % 2 == 1:
		correct_rects.append(rect)
		return area(rect[0], rect[1])

	# if discriminator % 2 == 0:
	# 	for y_bar in y_bars:
	# 		if (rect[1][0] >= y_bar[0][0] and rect[1][1] <= y_bar[0][1] and rect[0][1] == y_bar[1]):
	# 			correct_rects.append(rect)
	# 			print(rect, 'yon', y_bar)
	# 			return area(rect[0], rect[1])

	return 0

	# return int((sum(1 if rect[0][0] >= x_bar[0][0] and rect[0][1] <= x_bar[0][1] and rect[1][0] >= x_bar[1] else 0 for x_bar in x_bars)%2 == 1) or (rect[1][0] in list(map(lambda x_bar: x_bar[1], x_bars))))*area(rect[0], rect[1])

# def p(a):
# 	for line in a:
# 		print(''.join(['.' if c == 0 else '#' for c in line]))
# 	print()

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def tup_mul(a, c):
	return tuple(map(lambda elem: elem * c, a))



lines = list(map(lambda line: [dic[last_char_dic[line[2][len(line[2])-2]]], hex_to_int(line[2][2:len(line[2])-2])], lines))
# lines = list(map(lambda line: [dic[line[0]], int(line[1])], lines))


x_bars = []
y_bars = []
pos = (0,0)
points = []

for line in lines:
	if line[0] == (1,0):
		x_bars.append((pos, tup_add(pos, tup_mul(line[0], line[1]+1))))
	if line[0] == (-1, 0):
		x_bars.append((tup_add(pos, (1,0)), tup_add(pos, tup_mul(line[0], line[1]))))
	if line[0] == (0, 1):
		y_bars.append((pos, tup_add(pos, tup_mul(line[0], line[1]+1))))
	if line[0] == (0, -1):
		y_bars.append((tup_add(pos, (0,1)), tup_add(pos, tup_mul(line[0], line[1]))))
	pos = tup_add(pos, tup_mul(line[0], line[1]))
	points.append(pos)


print('initial x_bars:\n', x_bars)
# (x_interval tuple, y_height)
x_bars = [tuple(sorted(list(x_bar))) for x_bar in x_bars]
print('next x_bars:\n', x_bars)
x_bars = [((x_bar[0][0], x_bar[1][0]), x_bar[0][1]) for x_bar in x_bars]

print('y_bars:\n', y_bars)
y_bars = [tuple(sorted(list(y_bar), key = lambda t: t[1])) for y_bar in y_bars]
print('y_bars:\n', y_bars)
y_bars = [((y_bar[0][1], y_bar[1][1]), y_bar[0][0]) for y_bar in y_bars]
print('y_bars:\n', y_bars)


# x_bars = list(map(lambda t_tup: ((t_tup[0][0], t_tup[0][1]), t_tup[1][0]), x_bars))[1:] #might not need end bit here
# x_bars = sorted(x_bars, key = lambda t: t[1])

# x_dots = sorted(list(set(map(lambda point: point[0], points))))
# y_dots = sorted(list(set(map(lambda point: point[1], points))))

x_dots = sorted(list(set(reduce(lambda a,b: a+b, list(map(lambda point: [point[0], point[0]+1], points))))))
y_dots = sorted(list(set(reduce(lambda a,b: a+b, list(map(lambda point: [point[1], point[1]+1], points))))))

# x_dots = [[p, p+1] for ]
# x_dots = reduce(lambda a,b: [a]+[a+1])


x_intervals = [(x_dots[i], x_dots[i+1]) if i+1 < len(x_dots)-1 else (x_dots[i], x_dots[i]+1) for i in range(len(x_dots)-1)]
y_intervals = [(y_dots[i], y_dots[i+1]) if i+1 < len(y_dots)-1 else (y_dots[i], y_dots[i]+1) for i in range(len(y_dots)-1)]

#could use more checks
# def check_x_bar(rect):
# 	if (rect[0][1]-rect[0][0] == 1) and 

def check_y_bar(rect):
	return (rect[1][1]-rect[1][0] == 1)

def rect_is_edge(rect):
	if (rect[1][1]-rect[1][0] != 1) and (rect[0][1]-rect[0][0] != 1):
		return False

	for x_bar in x_bars:
		if rect[0][0] >= x_bar[0][0] and rect[0][1] <= x_bar[0][1] and rect[1][0] == x_bar[1]:
			return True

	for y_bar in y_bars:
		if rect[1][0] >= y_bar[0][0] and rect[1][1] <= y_bar[0][1] and rect[0][0] == y_bar[1]:
			return True

	assert(True)



# here a rectangle is described by two ranges
rects = [(x_int, y_int) for x_int in x_intervals for y_int in y_intervals]

edges = list(filter(lambda rect: rect_is_edge(rect), rects))
# print("CHECK X BAR:", check_x_bar(rects[0]))
rects = list(filter(lambda rect: not rect_is_edge(rect), rects))

print('lines:\n', lines)
print()
print('x_dots:\n', x_dots)
print('y_dots:\n', y_dots)
print()
print('x_intervals:\n', x_intervals)
print('y_intervals:\n', y_intervals)
print()
print('x_bars:\n', x_bars)
print('y_bars:\n', y_bars)
print()
print('rects:\n', rects)

assert(len(set(x_bars)) == len(x_bars))
assert(len(set(x_dots)) == len(x_dots))
assert(len(set(y_dots)) == len(y_dots))

assert(len(set(rects)) == len(rects))


def range_len(ran):
	return ran[1]-ran[0]

ans = sum(contribution(rect, x_bars, y_bars) for rect in rects)

ans += sum(range_len(x_bar[0]) for x_bar in x_bars)
ans += sum(range_len(y_bar[0]) for y_bar in y_bars)
ans -= len(lines)

# assert(len(y_bars) > 0)
# ans += sum(max(0, y_bar[0][1]-y_bar[0][0]) for y_bar in y_bars)

# print('rects:\n', rects)

for i in range(len(y_bars)-2):
	assert(y_bars[i][1] != y_bars[i+1][1]-1)


print('\nANSWER:', ans, '\n')
# print((x_dots[len(x_dots)-1]-x_dots[0])*(y_dots[len(y_dots)-1]-y_dots[0]))
# print('\n\n\n', rects[0])


# for rect in correct_rects:
# 	print(rect)

#mine:952404401494
#mine:952406747515
#mine:952408991563
#mine:952406747514
#real:952408144115


# # debugging
grid_size = 12
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

assert(len(set(correct_rects)) == len(correct_rects))
assert(len(set(rects)) == len(rects))

# rects = list(filter(lambda rect: rect_is_edge(rect), rects))
if (max(x_dots) < 12):
	for rect in edges:
		for x in range(rect[0][0], rect[0][1]):
			for y in range(rect[1][0], rect[1][1]):
				grid[y][x] += 1

	p(grid)

	grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
	for rect in correct_rects:
		for x in range(rect[0][0], rect[0][1]):
			for y in range(rect[1][0], rect[1][1]):
				grid[y][x] += 1

	p(grid)





#correct:
#952408144115
#952410806755-952408144115
#952408434107

#952403076474


#952404401494

#1049080731609


#1049080731609-952408144115
# 952408144115

#1049079059742