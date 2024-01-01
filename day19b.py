f = open('input.txt', 'r')
lines = f.read().split('\n\n')
l_dic = {'x': 0, 'm': 1, 'a': 2, 's': 3}
oper_dic = {'<': -1, '>': 1}

pre_workflows = lines[0] # yes I know this is awful (or awesome depends I guess)
pre_workflows = pre_workflows.split('\n')
workflow_defaults = [workflow[:-1].split(',')[-1] for workflow in pre_workflows]
workflow_names = [workflow.split('{')[0] for workflow in pre_workflows]
workflow_names += ['A', 'R'] # this is cheeky and a little dumb
workflow_rules = [workflow.split('{')[1].split(',')[:-1] for workflow in pre_workflows]
workflow_rules = [[rule.split(':') for rule in workflow] for workflow in workflow_rules]
workflow_rules = [[((l_dic[rule[0][0]], oper_dic[rule[0][1]], int(rule[0][2:])), rule[1]) for rule in workflow] for workflow in workflow_rules]

part = (range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))

def sign(i):
	if i > 0:
		return 1
	if i < 0:
		return -1
	return 0


# print('\nworkflow_defaults:', workflow_defaults)
print('\nworkflow_names:', workflow_names)
# print('\nworkflow_rules:', workflow_rules)

#         -1
# (1,2223) < 2222  X
#         -1
# (1,2222) < 2222  Y
#         -1
# (1,2221) < 2222  Y



#             1
# (2223,4000) > 2222  Y
#             1
# (2222,4000) > 2222  X
#             1
# (2221,4000) > 2222  X

# (1,10) > 5
#-> (1,5) (6,10)

# (1,10) < 5
#-> (1,5) (6,10)

def split_part(part, part_index, slice_index):
	arr = []
	arr.append(list(part))
	arr.append(list(part))
	arr[0][part_index] = range(part[part_index].start, slice_index)
	arr[1][part_index] = range(slice_index, part[part_index].stop)
	return [tuple(arr[0]), tuple(arr[1])]

from math import prod
def comb(part):
	return prod(r.stop-r.start for r in part)

def is_empty(part):
	return comb(part) == 0

index_A = workflow_names.index('A')
index_R = workflow_names.index('R')

import sys
print(sys.getrecursionlimit())

# (1351,4001) < 1351

ans_set = set()
def next_wf(part, curr_index, i2):
	print(part, curr_index, i2)
	# if curr_index == 7:
	# 	exit()

	# base cases
	if is_empty(part):
		print(part, 'reached Empty')
		return 0
	elif curr_index == index_A:

		global ans_set
		ans_set.add(part)
		# print(part, 'reached Acceptance')
		return comb(part)
	elif curr_index == index_R:
		# print(part, 'reached Rejection')
		return 0
	else:
		for i, rule in enumerate(workflow_rules[curr_index][i2:]):
			print(i)
			if rule[0][1] == 1 and sign(part[rule[0][0]].start+1-rule[0][2]) == 1:
					# print('case 1')
					return next_wf(part, workflow_names.index(rule[1]), 0)
			elif rule[0][1] == -1 and sign(part[rule[0][0]].stop-1-rule[0][2]) == -1:
					# print('case -1')
					return next_wf(part, workflow_names.index(rule[1]), 0)
			elif (rule[0][1] == 1 and (part[rule[0][0]].start < rule[0][2]+1 < part[rule[0][0]].stop)) or (rule[0][1] == -1 and (part[rule[0][0]].start < rule[0][2]-1 < part[rule[0][0]].stop)):
				# print('in else')
				sp = []
				if rule[0][1] == 1:
					sp = split_part(part, rule[0][0], rule[0][2]+1)
				if rule[0][1] == -1:
					sp = split_part(part, rule[0][0], rule[0][2])
				assert(len(sp) == 2)
				if rule[0][1] == -1:
					# part = sp[1]
					return next_wf(sp[1], curr_index, i+1) + next_wf(sp[0], workflow_names.index(rule[1]), 0)
				elif rule[0][1] == 1:
					# part = sp[0]
					return next_wf(sp[0], curr_index, i+1) + next_wf(sp[1], workflow_names.index(rule[1]), 0)
		# print('reached end')
		return next_wf(part, workflow_names.index(workflow_defaults[curr_index]), 0)



ans = next_wf(part, workflow_names.index('in'), 0)
print('ans:', ans)

ans = sum(comb(part) for part in ans_set)
print('ans:', ans)

# print('\n\n')
# print(len(ans_set))
# for a in ans_set:
# 	print(a)
# print('\n\n')



# def contribution(part, workflow_rules, workflow_defaults, workflow_names):
# 	curr_wf = 'in'

# 	while curr_wf != 'A':
# 		curr_wf_index = workflow_names.index(curr_wf)
# 		curr_rules = workflow_rules[curr_wf_index]
# 		curr_wf = next_wf(part, curr_rules, workflow_defaults, curr_wf_index)

# 		if curr_wf == 'R':
# 			return 0

# 	return sum(part)

# ans = sum(contribution(part, workflow_rules, workflow_defaults, workflow_names) for part in parts)
# print(ans)

#167409079868000
#167474394229030