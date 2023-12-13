f = open('input.txt', 'r')
lines = f.read().split('\n\n')
patterns = [list(map(list, line.split('\n'))) for line in lines]

def transpose(m):
	return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


# given y check that all rows [0...y] match rows [y+1...n]
def check_h_reflection(m, y):
	i = 0
	while y-i >= 0 and y+i+1 < len(m):
		if m[y-i] != m[y+i+1]:
			return False
		i += 1

	return True

# returns zero indexed row above reflection or -1 for none
def find_h_reflection(m):
	for y in range(len(m)-1):
		if check_h_reflection(m, y):
			return y

	return -1

def pattern_val(m):
	h_ref = find_h_reflection(m)
	if h_ref != -1:
		return 100*(h_ref+1)

	v_ref = find_h_reflection(transpose(m))
	if v_ref != -1:
		return (v_ref+1)

ans = 0
for pattern in patterns:
	ans += pattern_val(pattern)
print(ans)