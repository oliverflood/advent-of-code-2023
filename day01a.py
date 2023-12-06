def calibration_val(s):
	res = [int(i) for i in list(s) if i.isdigit()]
	return int(str(res[0]) + str(res[len(res)-1]))

f = open("input.txt", "r")
lines = f.read().split("\n")
ans = sum(list(map(calibration_val, lines)))

print(ans)