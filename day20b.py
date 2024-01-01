from graphviz import Digraph 
from collections import defaultdict
from copy import deepcopy
f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split(' -> ') for line in lines]
modules = tuple(((line[0][0], line[0][1:]) if line[0][0] != 'b' else ('0', 'broadcaster'),line[1].split(', ')) for line in lines)
module_names = tuple(module[0][1] for module in modules)

print(modules)

conjs = []
ffs = []
for module in modules:
	if module[0][0] == '&':
		conjs.append(module[0][1])
	if module[0][0] == '%':
		ffs.append(module[0][1])

def find_all_inputs(node, modules):
	arr = []
	for module in modules:
		if node in module[1]:
			arr.append(module[0][1])
	return arr

# map from conjunction name to input names
module_inputs = {module_name: find_all_inputs(module_name, modules) for module_name in module_names}
# conjuction_inputs = {module_name: {parent:0 for parent in module_inputs[module_name]} for module_name in module_names}
conjuction_inputs = [[0 for parent in module_inputs[module_name]] for module_name in module_names]
flip_flop_val = [0 for name in module_names]


outputs = {module[0][1]: module[1] for module in modules}
outputs = defaultdict(lambda: [], outputs)

# 0 -> low
# 1 -> high

# example module:
# (('0', 'broadcaster'), ['a', 'b', 'c'])

# example pulse:
# (index_to, strength, index_from)


# print(module_inputs)

rx_counts = [0,0]

def press_button(module_inputs, conjuction_inputs, flip_flop_val, start, c):
	pulses = []

	pulses.append((module_names.index(start), 0, -1))

	def append_to_pulses(next_name, strength, from_index, module_names):
		if next_name == 'pk':
			rx_counts[strength] += 1
			if strength == 0:
				print('added at ', c)
		if next_name in module_names:
			pulses.append((module_names.index(next_name), strength, from_index))
		else:
			pulses.append((-1, strength, from_index))

	while len(pulses) > 0:
		curr_pulse = pulses[0]
		del pulses[0]

		pulse_name = module_names[curr_pulse[0]]
		module_index = curr_pulse[0]
		pulse_strength = curr_pulse[1]
		curr_module = modules[module_index]

		# if curr_pulse[2] == -1:
		# 	print('button', '-low->' if pulse_strength == 0 else '-high->', pulse_name)
		# else:
		# 	print(module_names[curr_pulse[2]], '-low->' if pulse_strength == 0 else '-high->', pulse_name)

		# print(curr_pulse)


		if module_index == -1:
			continue

		if curr_module[0][0] == '%' and pulse_strength == 0:
			flip_flop_val[module_index] = 1-flip_flop_val[module_index]

		if curr_module[0][0] == '&':
			# print(curr_pulse)
			# print('curr_pulse[2]', curr_pulse[2])
			# print('module_names.index(curr_pulse[2]):', module_names[curr_pulse[2]])
			# print()
			conjuction_inputs[curr_pulse[0]][module_inputs[pulse_name].index(module_names[curr_pulse[2]])] = pulse_strength

		for next_module_name in curr_module[1]:
			match curr_module[0][0]:
				case '%':
					if pulse_strength == 0:
						append_to_pulses(next_module_name, flip_flop_val[module_index], module_index, module_names)
				case '&':
					if sum(conjuction_inputs[curr_pulse[0]]) == len(conjuction_inputs[curr_pulse[0]]):
						append_to_pulses(next_module_name, 0, module_index, module_names)
					else:
						append_to_pulses(next_module_name, 1, module_index, module_names)
				case '0':
					append_to_pulses(next_module_name, pulse_strength, module_index, module_names)


def image(ff):
	arr = []
	for item in ffs:
		arr.append(ff[module_names.index(item)])
	arr = ['#' if x == 1 else '.' for x in arr]
	return ''.join(arr)

def image_c(cnj):
	conjunctions = []
	for item in conjs:
		conjunctions.append(cnj[module_names.index(item)])

	arr = [['#' if x == 1 else '.' for x in item] for item in conjunctions]
	arr = [''.join(item) for item in arr]
	arr = ' '.join(arr)
	return arr

def full_image(ff, cnj):
	return image(ff)+'   '+image_c(cnj)

# prev_conjunctions = [image_c(conjuction_inputs)]
# prev_flip_flops = [image(flip_flop_val)]


# end = 2**10-1

# arr = []

# # conjuction_inputs = [[1 for _ in item] for item in conjuction_inputs]
# conjuction_inputs[module_names.index('cz')][find_all_inputs('cz', modules).index('dn')] = 0
# # flip_flop_val = [1 for _ in flip_flop_val]
# # conjuction_inputs = [[1 for _ in item] for item in conjuction_inputs]

# prev_state = [full_image(flip_flop_val, conjuction_inputs)]
# for c in range(1,end+1):
# 	if c%100 == 0:
# 		print(c)
# 	press_button(module_inputs, conjuction_inputs, flip_flop_val)
# 	arr.append((image_c(conjuction_inputs).count('#'), c, image_c(conjuction_inputs)))
# 	# if (conjuction_inputs in prev_conjunctions):
# 	# 	print('\n', conjuction_inputs)
# 	# 	print('^^prev conj found')
# 	# if (flip_flop_val in prev_flip_flops):
# 	# 	print('\n',flip_flop_val)
# 	# 	print('^^prev flipflop found')
# 	if full_image(flip_flop_val, conjuction_inputs) in prev_state or sum(conjuction_inputs[41]) == len(conjuction_inputs[41]):
# 		print('\nPREV STATE:', c)
# 		print(full_image(flip_flop_val, conjuction_inputs))
# 		# print('PREV STATE^^ at', c, '\n')
# 		break
# 	prev_state.append(full_image(flip_flop_val, conjuction_inputs))

# 	if rx_counts[0] > 1:
# 		print("FOUND!!!", c)
# 		exit()


# print('\nprev_conjunctions:')
# for thing in prev_conjunctions:
# 	print(thing)
# print('\nprev_flip_flops:')
# for thing in prev_flip_flops:
# 	print(thing)

# cyclic_

# backup = [32, 256, 4, 8, 1, 1024, 128, 512, 2048]
# twos_array = [-1 for i in range(9)]
# print('\nprev_state:')
# for i, thing in enumerate(prev_state):

# 	if i==9993:
# 		print(i)
# 	print(thing, i)
# 	if thing[65:74] == '#'*9:
# 		print("BREAK")
# 		break
# 	for j in range(len(twos_array)):
# 		# if (i % (backup[j]*2) >= backup[j]):
# 		# 	assert(thing[65+j] == '#')
# 		if thing[65+j] == '#' and twos_array[j] == -1:
# 			twos_array[j] = i
# print()

# print(len(prev_state[0][:prev_state[0].index(' ')]))


# parent_set = set()
# def find_origin(name):
# 	if name == 'broadcaster':
# 		return

# 	for parent in find_all_inputs(name, modules):
# 		if parent in conjs or name == 'rx':
# 			parent_set.add(parent)
# 			print(parent)
# 			find_origin(parent)

# find_origin('rx')
# print(len(parent_set))

# print(ffs)
# print(conjs)
# print('0'*65)
# print(twos_array)

# print(max(arr))
# print(len(image_c(conjuction_inputs)))

# print(module_names.index('cz'))

# print(len(image(flip_flop_val)))

# 32 _ 4 8 2 _ _ _ _


# 65 73


#

#
 #
##
 #
##
#[32, 256, 4, 8, 1, 1024, 128, 512, 2048]	

def create_graph(node_map, graph_name='day20b', format='png', view=True):
	dot = Digraph(comment='Directed Graph')

	for parent, children in node_map.items():
		node_color = 'red' if parent in conjs else 'green'
		node_color = 'purple' if parent == 'rx' else node_color
		dot.node(parent, parent, color=node_color)

		for child in children:
			node_color = 'red' if child in conjs else 'green'
			node_color = 'purple' if child == 'rx' else node_color
			dot.node(child, child, color=node_color)
			dot.edge(parent, child)

	dot.save(f'{graph_name}.dot')
	dot.render(graph_name, format=format, view=view)


# create_graph(outputs)

print(ffs)
print(conjs)


def all_children(start, outputs):
	open_list = [start]
	visited = [start]
	while len(open_list) > 0:
		curr = open_list.pop()

		for neighbor in outputs[curr]:
			if neighbor in visited:
				continue
			open_list.append(neighbor)
			visited.append(neighbor)

	return visited

print(all_children('fs', outputs))

print(full_image(flip_flop_val, conjuction_inputs))
# press_button(module_inputs, conjuction_inputs, flip_flop_val, 'sh')


for c in range(1, 1000000):
	press_button(module_inputs, conjuction_inputs, flip_flop_val, 'nm', c)
	# print(rx_counts)
	# print(full_image(flip_flop_val, conjuction_inputs))
	if rx_counts[0] > 1:
		print("FOUND!!!", c, rx_counts)
		rx_counts[0] = 0
		# exit()

import math
print(math.lcm(4021, 4013, 3881, 3889))

# A: 4021
# B: 4013
# C: 3881
# D: 3889

# what god awful code this all is 