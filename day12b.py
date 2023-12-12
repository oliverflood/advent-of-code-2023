import re

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = list(map(lambda line: line.split(' '), lines))

# god awful way to get the right data
cases = [(((line[0]+'?')*5)[0:len(line[0])*5+4], tuple(map(int, line[1].split(',')))*5) for line in lines]

# check if a case is a valid arrangement
def is_valid(case):
	arr = re.findall(r'#+', case[0])
	arr = list(map(lambda s: len(s), arr))

	return arr == case[1]

# check if we can place a block of #'s at pos
def can_place(n, s, pos):
	# can we even fit
	if n > len(s[pos: pos+n]):
		return False

	# do we overlap over dots
	if s[pos: pos+n].count('.') > 0:
		return False

	# are we bounded by dots
	if pos-1 >= 0 and s[pos-1] == '#':
		return False
	if pos+n < len(s) and s[pos+n] == '#':
		return False
	return True

# dynamic programming 
memo = {}
# count number of arrangements
def arrangements(case):
	# if we've seen it before we don't have to recalculate
	if case in memo:
		return memo[case]
	
	# base case: no more blocks to place
	if len(case[1]) == 0:
		# if nothing left to cover we can count it
		if case[0].count('#') == 0:
			return 1
		# otherwise not a valid case
		return 0

	ans = 0
	# recurse when we can place our first block
	for i in range(len(case[0])):
		if can_place(case[1][0], case[0], i):
			ans += arrangements((case[0][case[1][0]+i+1:], case[1][1:]))
		# stop recursing once we miss a block
		if case[0][0:i].count('#') > 0:
			break

	#update memo before returning answer
	memo[case] = ans
	return ans


# B)
ans = sum(list(map(arrangements, cases)))
print(ans)
