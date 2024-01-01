import re

class Trajectory():
	def __init__(self, px, py, vx, vy):
		self.px = px
		self.py = py
		self.vx = vx
		self.vy = vy

	def print(self):
		print('p', self.px, '  ', self.py, 'v', self.vx, '  ', self.vy)

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split(', ') for line in lines]
lines = list(map(lambda line: line[0:2] + line[2].split(' @ ') + line[3:], lines))
lines = [list(map(int, line)) for line in lines]
trajectories = [Trajectory(line[0], line[1], line[3], line[4]) for line in lines]
# lines = [Line(line[0], line[1], line[0]+line[3], line[1]+line[4]) for line in lines]

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def tup_mul(a, c):
	return tuple(map(lambda elem: elem * c, a))

def tup_sub(a, b):
	return tup_add(a, tup_mul(b, -1))

# for t in trajectories:
# 	t.print()

#assuming no colinear paths

# 2d cross product
def cross_2d(vec1, vec2):
	return vec1[0]*vec2[1]-vec1[1]*vec2[0]

# takes two trajectories, returns whether they intersect
def do_intersect(t1, t2):
	p = (t1.px, t1.py)
	q = (t2.px, t2.py)
	r = (t1.vx, t1.vy)
	s = (t2.vx, t2.vy)

	if cross_2d(r, s) != 0:
		t = cross_2d(tup_sub(q, p), s) / cross_2d(r, s)
		u = cross_2d(tup_sub(p, q), r) / cross_2d(s, r)
		if t >= 0 and u >= 0:
			return True
	return False

# takes two trajectories, returns point of intersection
def int_point(t1, t2):
	p = (t1.px, t1.py)
	q = (t2.px, t2.py)
	r = (t1.vx, t1.vy)
	s = (t2.vx, t2.vy)

	if cross_2d(r, s) != 0:
		t = cross_2d(tup_sub(q, p), s) / cross_2d(r, s)
		u = cross_2d(tup_sub(p, q), r) / cross_2d(s, r)
		# print('t:', t)
		# print('u:', u)
		return tup_add(p, tup_mul(r, t))

def in_bounds(point, bounds):
	if bounds[0] <= point[0] <= bounds[1]:
		if bounds[0] <= point[1] <= bounds[1]:
			return True
	return False

bounds = (200000000000000,400000000000000)

ans = 0

for i, t1 in enumerate(trajectories):
	for j, t2 in enumerate(trajectories):
		if i >= j:
			continue
		if do_intersect(t1, t2):
			# print()
			# t1.print()
			# t2.print()
			point = int_point(t1, t2)
			if in_bounds(point, bounds):
				ans += 1
				# print('at point', point)

print(ans)