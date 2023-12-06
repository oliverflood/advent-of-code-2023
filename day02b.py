import math
colors = ['red', 'green', 'blue']

def extract_colors(arr):
	counts = [next((int(s.split(' ')[0]) for s in arr if s.find(colors[i]) != -1), 0) 
			 for i in range(3)]
	return counts


def extract_line(s):
	# chop off game number
	s = s[s.find(':') + 2:]

	# split by reveal
	reveals = s.split('; ')

	# split reveals by r,g,b string trios
	reveals = [reveal.split(', ') for reveal in reveals]

	# extract color values in [r,g,b] order
	return list(map(extract_colors, reveals))


def power(game):
	# game is an array of [r,g,b] triplets
	return math.prod([max([rgb[i] for rgb in game]) for i in range(3)])


f = open('input.txt', 'r')
lines = f.read().split('\n')

games = list(map(extract_line, lines))

ans = sum([power(game) for game in games])
print(ans)