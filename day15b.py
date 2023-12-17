from copy import deepcopy
f = open('input.txt', 'r')
strings = f.read().split(',')

# compute the hash of a string
def hash(s):
	ans = 0
	for char in s:
		ans += ord(char)
		ans *= 17
		ans %= 256
	return ans

# compute the total focusing power of a list of boxes
def power(boxes): 
	arr = [sum((i+1)*boxes[b_n][i][1] for i in range(len(boxes[b_n]))) for b_n in range(len(boxes))]
	return sum((j+1)*arr[j] for j in range(len(arr)))

# array of boxes (lists) of tuple pairs (string, int)
boxes = [[] for x in range(256)]

for s in strings:
	if '=' in s:
		sp = s.split('=')
		h = hash(sp[0])
		boxes_labels = list(map(lambda tup: tup[0], boxes[h]))

		# case where label exists already
		if sp[0] in boxes_labels:
			boxes[h][boxes_labels.index(sp[0])] = (sp[0], int(sp[1]))

		# case where label new 
		else:
			boxes[h].append((sp[0], int(sp[1])))

	if '-' in s:
		sp = s[:len(s)-1]
		h = hash(sp)
		boxes_labels = list(map(lambda tup: tup[0], boxes[h]))

		if sp in boxes_labels:
			del boxes[h][boxes_labels.index(sp)]

ans = power(boxes)
print(ans)