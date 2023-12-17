from copy import deepcopy
f = open('input.txt', 'r')
strings = f.read().split(',')

def hash(s):
	ans = 0
	for char in s:
		ans += ord(char)
		ans *= 17
		ans %= 256
	return ans

print(sum(hash(s) for s in strings))