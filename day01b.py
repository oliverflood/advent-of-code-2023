words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def find_first_digit(s):
	w_indexes = [float('inf') if s.find(x) == -1 else s.find(x) for x in words]
	d_indexes = [float('inf') if s.find(str(x)) == -1 else s.find(str(x)) for x in range(1,10)]
	
	w = min(w_indexes)
	d = min(d_indexes)

	if (d < w):
		return d_indexes.index(d) + 1
	return w_indexes.index(w) + 1


def find_last_digit(s):
	w_indexes = [s.rfind(x) for x in words]
	d_indexes = [s.rfind(str(x)) for x in range(1,10)]
	
	w = max(w_indexes)
	d = max(d_indexes)

	if (d > w):
		return d_indexes.index(d) + 1
	return w_indexes.index(w) + 1
		

def calibration_val(s):
	return int(str(find_first_digit(s)) + str(find_last_digit(s)))


f = open("input.txt", "r")
lines = f.read().split("\n")

ans = sum(list(map(calibration_val, lines)))
print(ans)