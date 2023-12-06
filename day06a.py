import re

f = open('input.txt', 'r')
sections = f.read().split('\n')

times = list(map(int, re.findall(r'\d+', sections[0])))
distances = list(map(int, re.findall(r'\d+', sections[1])))

# lol simple
prod = 1
for i in range(len(times)):
	for x in range(times[i]+1):
		if (times[i]-x)*(times[i]-(times[i]-x)) > distances[i]:
			prod *= times[i]+1-x*2
			break

print(prod)
