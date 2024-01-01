f = open('input.txt', 'r')
lines = f.read().split('\n\n')
l_dic = {'x': 0, 'm': 1, 'a': 2, 's': 3}
oper_dic = {'<': -1, '>': 1}

pre_workflows = lines[0] # yes I know this is awful (or awesome depends I guess)
pre_workflows = pre_workflows.split('\n')
workflow_defaults = [workflow[:-1].split(',')[-1] for workflow in pre_workflows]
workflow_names = [workflow.split('{')[0] for workflow in pre_workflows]
workflow_rules = [workflow.split('{')[1].split(',')[:-1] for workflow in pre_workflows]
workflow_rules = [[rule.split(':') for rule in workflow] for workflow in workflow_rules]
workflow_rules = [[((l_dic[rule[0][0]], oper_dic[rule[0][1]], int(rule[0][2:])), rule[1]) for rule in workflow] for workflow in workflow_rules]

parts = lines[1] # less awful
parts = parts.split('\n')
parts = [tuple([int(val[2:]) for val in part[1:-1].split(',')]) for part in parts]

# print('\nparts:', parts)
# print('\nworkflow_defaults:', workflow_defaults)
# print('\nworkflow_names:', workflow_names)
# print('\nworkflow_rules:', workflow_rules)

def sign(i):
	if i > 0:
		return 1
	if i < 0:
		return -1
	return 0

def next_wf(part, rules, defaults, curr_index):
	for rule in rules:
		if sign(part[rule[0][0]]-rule[0][2]) == rule[0][1]:
			return rule[1]

	return defaults[curr_index]

def contribution(part, workflow_rules, workflow_defaults, workflow_names):
	curr_wf = 'in'

	while curr_wf != 'A':
		curr_wf_index = workflow_names.index(curr_wf)
		curr_rules = workflow_rules[curr_wf_index]
		curr_wf = next_wf(part, curr_rules, workflow_defaults, curr_wf_index)

		if curr_wf == 'R':
			return 0

	return sum(part)

ans = sum(contribution(part, workflow_rules, workflow_defaults, workflow_names) for part in parts)
print(ans)