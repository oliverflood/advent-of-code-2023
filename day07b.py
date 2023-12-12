from functools import cmp_to_key
convert = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

# convert a hand to a list of numbers with respective values
def hand_convert(s):
	assert(len(s) == 5)
	ans = []

	for letter in list(s):
		ans.append(convert.index(letter)+1)

	return ans

# discriminate between types of hands
def discriminator(hand):
	# case "JJJJJ"
	if (hand == [1,1,1,1,1]):
		return 25

	# find most popular non-jack element
	nj_hand = list(filter(lambda n: n != 1, hand))
	most_pop = max(set(nj_hand), key=nj_hand.count)

	new_hand = [most_pop if n == 1 else n for n in hand]

	return sum(list(map(lambda num: new_hand.count(num), new_hand)))

# discriminate between two of same type of hands
def disc2(hand):
	ans = 0
	for i, n in enumerate(hand):
		ans += (20**(4-i))*n
	return ans

def pair_compare(pair_a, pair_b):
	hand_a = pair_a[0]
	hand_b = pair_b[0]

	# hands diff type
	if (discriminator(hand_a) < discriminator(hand_b)):
		return -1
	if (discriminator(hand_a) > discriminator(hand_b)):
		return 1

	# hands same type
	if (disc2(hand_a) < disc2(hand_b)):
		return -1
	if (disc2(hand_a) > disc2(hand_b)):
		return 1

	return 0


# start
f = open('input.txt', 'r')
lines = f.read().split('\n')
pairs = list(map(lambda line: line.split(' '), lines))
pairs = list(map(lambda pair: (hand_convert(pair[0]), int(pair[1])), pairs))

pairs = sorted(pairs, key = cmp_to_key(pair_compare))

ans = 0
for i, pair in enumerate(pairs):
	ans += (i+1)*pair[1]
print(ans)

# print(list(map(lambda a: discriminator(a[0]), pairs)))
# print(list(map(lambda a: disc2(a[0]), pairs)))