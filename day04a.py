import re

class Card:
	def __init__(self, winners, yours):
		self.winners = winners
		self.yours = yours

f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = list(map(lambda line: line[8:].split(' | '), lines))


card_list = []
for line in lines:
	card_list.append(Card(re.findall(r'\d+', line[0]), re.findall(r'\d+', line[1])))

# count up the values of each card (based on number of matches)
card_values = []
for card in card_list:
	card_count = 0
	for winner in card.winners:
		if (winner in card.yours):
			card_count += 1
	card_values.append(card_count)

# start with one of each card
card_totals = [1]*len(card_list)

# give ourselves new cards based on card counts
for i, value in enumerate(card_values):
	for x in range(value):
		if i+x+1 <= len(card_totals)-1:
			card_totals[i+x+1] += card_totals[i]

# ans is sum of cards
ans = sum(card_totals)
print(ans)