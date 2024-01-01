from copy import deepcopy
f = open('input.txt', 'r')
lines = f.read().split()
lines = [list(line) for line in lines]
beams = [[[] for _ in range(len(lines[0]))] for _ in range(len(lines))] # careful with copies!
visited = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]

# \ : (1,0)->(0,1) (0,-1)->(-1,0) (0,1)->(1,0) (0,-1)->(-1,0) flip 
# / : (1,0)->(0,-1) (0,-1)->(1,0) etc flip + sign
# - : (0,1) or (0,-1)->(1,0),(-1,0) 
# | : (1,0) or (-1,0)->(0,1),(-1,0)

d = {'\\': {(1,0):[(0,1)], (0,-1):[(-1,0)], (0,1):[(1,0)], (-1,0):[(0,-1)]}, 
	  '/': {(1,0):[(0,-1)], (0,-1):[(1,0)], (0,1):[(-1,0)], (-1,0):[(0,1)]},
	  '-': {(0,1):[(1,0),(-1,0)], (0,-1):[(1,0),(-1,0)], (1,0):[(1,0)], (-1,0):[(-1,0)]}, 
	  '|': {(1,0):[(0,1),(0,-1)], (-1,0):[(0,1),(0,-1)], (0,-1):[(0,-1)], (0,1):[(0,1)]}, 
	  '.': {(1,0):[(1,0)], (-1,0):[(-1,0)], (0,1):[(0,1)], (0,-1):[(0,-1)]}}

beams[0][0].append((1, 0))
visited[0][0] = 1

def step_beams(b):
	new_beams = [[[] for _ in range(len(lines[0]))] for _ in range(len(lines))]

	for x in range(len(b[0])):
		for y in range(len(b)):
			for beam in b[y][x]:
				for new_beam in d[lines[y][x]][beam]:
					# bound check
					if x+new_beam[0] < 0 or x+new_beam[0] >= len(new_beams[0]) or y+new_beam[1] < 0 or y+new_beam[1] >= len(new_beams):
						break

					# update new list of beams and visit square
					new_beams[y+new_beam[1]][x+new_beam[0]].append(new_beam)
					visited[y+new_beam[1]][x+new_beam[0]] = 1

	new_beams = [[list(set(new_beams[y][x])) for x in range(len(new_beams[0]))] for y in range(len(new_beams))]

	return new_beams

def energized():
	return sum(sum(line) for line in visited)

def p(a):
	for line in a:
		print(str(line))
	print()

for x in range(1000):
	beams = step_beams(beams)

print(energized())
# p(visited)