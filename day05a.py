import re

def convert_seed(m, seed):
	for line in m:
		# if within source range
		if seed < line[1] + line[2] and seed >= line[1]:
			# return destination range start + offset
			return line[0] + (seed - line[1])
	return seed

def convert_all(m, seeds):
	return [convert_seed(m, seed) for seed in seeds]

def end_to_end(maps, seeds):
	for m in maps:
		seeds = convert_all(m, seeds)
	return seeds

f = open('input.txt', 'r')
sections = f.read().split('\n\n')

# scoop out seeds
seeds = re.findall(r'\d+', sections[0])
seeds = list(map(int, seeds))

# scoop out maps (as arrays of our trios)
maps = [section.split('\n')[1:] for section in sections[1:]]
maps = list(map(lambda m: [list(map(int, s.split(' '))) for s in m], maps))

ans = min(end_to_end(maps, seeds))
print(ans)