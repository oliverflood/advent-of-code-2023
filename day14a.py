f = open('input.txt', 'r')
lines = list(map(list, f.read().split('\n')))

def total_column(x):
	ans = 0
	wallpos = -1

	for y in range(len(lines)):
		if lines[y][x] == 'O':
			wallpos += 1
			ans += len(lines)-wallpos
			
		if lines[y][x] == '#':
			wallpos = y

	return ans

ans = sum(total_column(x) for x in range(len(lines[0])))
print(ans)
