colors = ['red', 'green', 'blue']

r = 12
g = 13
b = 14

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


def is_possible(game):
	# game is an array of [r,g,b] triplets
	arr = list(map(lambda x: (x[0] <= r and x[1] <= g and x[2] <= b), game))
	return min(arr)


f = open('input.txt', 'r')
lines = f.read().split('\n')

games = list(map(extract_line, lines))

ans = sum([is_possible(games[i])*(i+1) for i in range(len(games))])
print(ans)

