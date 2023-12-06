import re
import math
import functools

f = open('input.txt', 'r')
sections = f.read().split('\n')

t = int(functools.reduce(lambda a,b: a+b, re.findall(r'\d+', sections[0])))
d = int(functools.reduce(lambda a,b: a+b, re.findall(r'\d+', sections[1])))

# we wish to find n when (t-n)(t-(t-n)) > d
# same as when -d+tn-n^2 > 0
# quadratic formula -> (-t+sqrt(t^2-4*d))/(-2))
# only have to care about one side since it's symmetric
# take ceiling of left side -> now we have n when (t-n)(t-(t-n)) > d first holds
# out of t+1 total possibilites we subtract n*2 (for two tails)

ans = t+1 - 2*math.ceil((-t+math.sqrt(t**2-4*d))/(-2))
print(ans)
# mmm very nice