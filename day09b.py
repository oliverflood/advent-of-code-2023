f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = list(map(lambda line: list(map(int, line.split(' ')))[::-1], lines))

def differences(arr):
	return [arr[i+1]-arr[i] for i in range(len(arr)-1)]

def extrapolate(arr):
	lists = [arr]

	# while not all zeros
	while lists[len(lists)-1] != [0] * len(lists[len(lists)-1]):
		lists.append(differences(lists[len(lists)-1]))

	return arr[len(arr)-1] + sum(list(map(lambda arr: arr[len(arr)-1]-arr[len(arr)-2], lists)))

ans = sum(list(map(extrapolate, lines)))
print(ans)