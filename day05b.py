import re
from decimal import Decimal

# returns intersection of two ranges (which is a range)
def range_intersect(r1, r2):
    return range(max(r1.start,r2.start), min(r1.stop,r2.stop)) or None

# shift range by d units
def range_shift(r, d):
	return range(r.start + d, r.stop + d)

# returns array of ranges: removes intersection of r1, r2 from r1
def range_remove(r1, r2):
	ans = []
	intersection = range_intersect(r1, r2)
	if (intersection == None):
		return [r1]

	left = range(0, intersection.start)
	right = range(intersection.stop, 10**20) #basically infinity

	left = range_intersect(left, r1)
	right = range_intersect(right, r1)

	if (left != None):
		ans.append(left)
	if (right != None):
		ans.append(right)

	return ans

# convert ranges into refined, shifted ones
def convert_all(m, ranges):
	# note: m is an array of tuples: (start range, shift amount)
	ans = []

	# for each seed range
	for r in ranges:
		# for each mapping (start range -> shift amount)
		untouched = True # <- check if range is unmapped

		for tup in m:
			start_range = tup[0]
			shift_amount = tup[1]
			intersection = range_intersect(start_range, r)

			# test if we map anything
			if (intersection != None):
				untouched = False
				ans.append(range_shift(intersection, shift_amount))
				# add in any newly separated ranges
				ranges += range_remove(r, intersection)

		if (untouched): # <- if range is unmapped we add it to answer
			ans.append(r)

	# return ans
	return list(set(ans)) # NEEDS REFACTORING- this shouldn't need to be done

# go through all maps
def end_to_end(maps, ranges):
	for m in maps:
		ranges = convert_all(m, ranges)
	return ranges


f = open('input.txt', 'r')
sections = f.read().split('\n\n')

# scoop out seeds
seeds = re.findall(r'\d+', sections[0])
seeds = list(map(int, seeds))

seed_ranges = []
for i in range(int(len(seeds)/2)):
	seed_ranges.append(range(seeds[2*i], seeds[2*i]+seeds[2*i+1]))

# scoop out maps as arrays of tuples: (start range, shift amount)
maps = [section.split('\n')[1:] for section in sections[1:]]
maps = list(map(lambda m: [list(map(int, s.split(' '))) for s in m], maps))
maps = list(map(lambda m: [(range(s[1], s[1]+s[2]), s[0]-s[1]) for s in m], maps))


# NEEDS REFACTORING!!!

locs = []
for seed_range in seed_ranges:
	locations = end_to_end(maps, seed_ranges)
	locs.append(min(list(map(lambda x: x.start, locations))))

ans = min(locs)
print(ans)