import math

class Trajectory():
	def __init__(self, px, py, pz, vx, vy, vz):
		self.px = px
		self.py = py
		self.pz = pz
		self.vx = vx
		self.vy = vy
		self.vz = vz

	def print(self):
		print('p', self.px, self.py, self.pz, '  v', self.vx, self.vy, self.vz)

	def eq(self):
		print('(', self.px, ',', self.py, ',', self.pz, ')+t*(',self.vx, ',', self.vy, ',', self.vz, ')')

	def pos_at_time(self, t):
		return (self.px + t*self.vx, self.py + t*self.vy, self.pz + t*self.vz)


f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split(', ') for line in lines]
lines = list(map(lambda line: line[0:2] + line[2].split(' @ ') + line[3:], lines))
lines = [list(map(int, line)) for line in lines]
trajectories = [Trajectory(line[0], line[1], line[2], line[3], line[4], line[5]) for line in lines]

def tup_add(a, b):
	return tuple(map(sum, zip(a, b)))

def tup_mul(a, c):
	return tuple(map(lambda elem: elem * c, a))

def tup_sub(a, b):
	return tup_add(a, tup_mul(b, -1))

def tup_div(a, c):
	return tuple(map(lambda elem: elem / c, a))

# for i, t in enumerate(trajectories):
# 	print('L_{', end='')
# 	print(i, end='')
# 	print('} = ', end='')
# 	t.eq()


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

def v_transform(tr, vx, vy, vz):
	return Trajectory(tr.px, tr.py, tr.pz, tr.vx-vx, tr.vy-vy, tr.vz-vz)

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

# # Bezout's identity
# want to check
# p2 - p1 % gcd(v1-vs, v2-vs) == 0
# if this is false then throw out vs (this must hold for all trajectories, for the three vs's in x,y, and z)
# def check_intersect_x(trajs, vs):
# 	for i in range(len(trajs)-2):
# 		if abs(trajs[i].px -trajs[i+1].px) % math.gcd(trajs[i].vx - vs, trajs[i+1].vx - vs) != 0:
# 			return False
# 	return True


# takes two trajectories, returns point of intersection
def zint_point(t1, t2):
	p = (t1.px, t1.pz)
	q = (t2.px, t2.pz)
	r = (t1.vx, t1.vz)
	s = (t2.vx, t2.vz)

	if cross_2d(r, s) != 0:
		t = cross_2d(tup_sub(q, p), s) / cross_2d(r, s)
		u = cross_2d(tup_sub(p, q), r) / cross_2d(s, r)
		# print('t:', t)
		# print('u:', u)
		return tup_add(p, tup_mul(r, t))

# takes two trajectories, returns whether they intersect
def zdo_intersect(t1, t2):
	p = (t1.px, t1.pz)
	q = (t2.px, t2.pz)
	r = (t1.vx, t1.vz)
	s = (t2.vx, t2.vz)

	if cross_2d(r, s) != 0:
		t = cross_2d(tup_sub(q, p), s) / cross_2d(r, s)
		u = cross_2d(tup_sub(p, q), r) / cross_2d(s, r)
		if t >= 0 and u >= 0:
			return True
	return False

def check_xy(trajectories, x, y):
	point = None
	for i in range(len(trajectories)-2):
		t1 = v_transform(trajectories[i], x, y, 0)
		t2 = v_transform(trajectories[i+1], x, y, 0)

		if not do_intersect(t1, t2):
			# print('dont intersect')
			return False

		next_point = int_point(t1, t2)
		if point != None and point != next_point:
			return False
		point = next_point

	return True

def zcheck_xz(trajectories, x, z):
	point = None
	for i in range(len(trajectories)-2):
		t1 = v_transform(trajectories[i], x, 0, z)
		t2 = v_transform(trajectories[i+1], x, 0, z)

		if not zdo_intersect(t1, t2):
			# print('dont intersect')
			return False

		next_point = zint_point(t1, t2)
		if point != None and point != next_point:
			return False
		point = next_point

	return True


RANGE = 400

finalx = 47
finaly = -360
# for x in range(-RANGE, RANGE):
# 	for y in range(-RANGE, RANGE):
# 		if check_xy(trajectories, x, y):

# 			print(x, y)
# 			finalx = x
# 			finaly = y

finalz = -1
for z in range(-RANGE, RANGE):
	if zcheck_xz(trajectories, finalx, z):
		print(z)
		finalz = z

t1 = trajectories[0]
t2 = trajectories[1]

px = int_point(v_transform(t1, finalx, finaly, finalz), v_transform(t2, finalx, finaly, finalz))[0]
py = int_point(v_transform(t1, finalx, finaly, finalz), v_transform(t2, finalx, finaly, finalz))[1]
pz = zint_point(v_transform(t1, finalx, finaly, finalz), v_transform(t2, finalx, finaly, finalz))[1]
print(px, py, pz)
ans = int(px+py+pz)
print(ans)

# print(check_xy(trajectories, -3, 1))




# print(check_intersect_x(trajectories, -3))
# for y in range(-200, 200):




# Hailstone A: 19@ -2
# Hailstone B: 18@ -1
# -3

# 19 + t*(-2+3)
# 18 + t*(-1+3)

# 19 + t
# 18 + 2t



# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1


# p1 @ v1
# p2 @ v2
# vs

# p1 + t1*(v1-vs) = p2 + t2*(v2-vs)
# p1 - p2 = t2v2 - t1v1 + t1vs - t2vs
# p1 - p2 = t2v2 - t1v1 + vs*(t1-t2

