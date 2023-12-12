import re

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = list(map(lambda line: line.split(' '), lines))
cases = [(line[0], list(map(int, line[1].split(',')))) for line in lines]

# check if a case is a valid arrangement
def is_valid(case):
	arr = re.findall(r'#+', case[0])
	arr = list(map(lambda s: len(s), arr))

	return arr == case[1]

# recurse through possible arrangements
def arrangements(case):
	if case[0].count('?') == 0:
		if (is_valid(case)):
			return 1
		else:
			return 0

	return arrangements((case[0].replace('?', '.', 1), case[1])) + arrangements((case[0].replace('?', '#', 1), case[1]))

# why not brute force it :)
ans = list(map(arrangements, cases))
print(ans)
