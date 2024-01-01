from copy import deepcopy
f = open('input.txt', 'r')
lines = f.read().split()
lines = [list(line) for line in lines]
NUM_ITERS = 700

# \ : (1,0)->(0,1) (0,-1)->(-1,0) (0,1)->(1,0) (0,-1)->(-1,0) flip 
# / : (1,0)->(0,-1) (0,-1)->(1,0) etc flip + sign
# - : (0,1) or (0,-1)->(1,0),(-1,0) 
# | : (1,0) or (-1,0)->(0,1),(-1,0)

d = {'\\': {(1,0):[(0,1)], (0,-1):[(-1,0)], (0,1):[(1,0)], (-1,0):[(0,-1)]}, 
	  '/': {(1,0):[(0,-1)], (0,-1):[(1,0)], (0,1):[(-1,0)], (-1,0):[(0,1)]},
	  '-': {(0,1):[(1,0),(-1,0)], (0,-1):[(1,0),(-1,0)], (1,0):[(1,0)], (-1,0):[(-1,0)]}, 
	  '|': {(1,0):[(0,1),(0,-1)], (-1,0):[(0,1),(0,-1)], (0,-1):[(0,-1)], (0,1):[(0,1)]}, 
	  '.': {(1,0):[(1,0)], (-1,0):[(-1,0)], (0,1):[(0,1)], (0,-1):[(0,-1)]}}

# prints out a visited matrix
def p(a):
	for line in a:
		print(''.join(['.' if c == 0 else '#' for c in line]))

def step_beams(b, visited):
	new_beams = set()

	for beam in b:
		x = beam[2]
		y = beam[3]

		for new_beam in d[lines[y][x]][(beam[0], beam[1])]:
			if not (x+new_beam[0] < 0 or x+new_beam[0] >= len(lines[0]) or y+new_beam[1] < 0 or y+new_beam[1] >= len(lines)):
				new_beams.add((new_beam[0], new_beam[1], x+new_beam[0], y+new_beam[1]))
				visited[y+new_beam[1]][x+new_beam[0]] = 1 

	return new_beams, visited

def energy(v):
	return sum(sum(line) for line in v)

def energy_from_start(start):
	visited = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]
	visited[start[3]][start[2]] = 1
	beams = set()
	beams.add(start)

	for x in range(NUM_ITERS):
		# print(x, energy(visited))
		beams, visited = step_beams(beams, visited)

	return energy(visited)

ans = []
for x in range(len(lines[0])):
	print(x)
	ans.append(energy_from_start((0,1,x,0)))
	ans.append(energy_from_start((0,-1,x,len(lines)-1)))

for y in range(len(lines)):
	print(y)
	ans.append(energy_from_start((1,0,0,y)))
	ans.append(energy_from_start((-1,0,len(lines[0])-1,y)))

print(max(ans))