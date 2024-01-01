f = open('input.txt', 'r')
lines = f.read().split('\n')
lines = [line.split(' -> ') for line in lines]
modules = tuple(((line[0][0], line[0][1:]) if line[0][0] != 'b' else ('0', 'broadcaster'),line[1].split(', ')) for line in lines)
module_names = tuple(module[0][1] for module in modules)

def find_all_inputs(node, modules):
	arr = []
	for module in modules:
		if node in module[1]:
			arr.append(module[0][1])
	return arr

# map from conjunction name to input names
module_inputs = {module_name: find_all_inputs(module_name, modules) for module_name in module_names}
conjuction_inputs = {module_name: {parent:0 for parent in module_inputs[module_name]} for module_name in module_names}
flip_flop_val = [0 for name in module_names]

# 0 -> low
# 1 -> high

# example module:
# (('0', 'broadcaster'), ['a', 'b', 'c'])

# example pulse:
# (index_to, strength, index_from)


counts = [0, 0]

def press_button(module_inputs, conjuction_inputs, flip_flop_val):
	pulses = []

	pulses.append((module_names.index('broadcaster'), 0, -1))
	counts[0]+=1

	def append_to_pulses(next_name, strength, from_index, module_names):
		if next_name in module_names:
			pulses.append((module_names.index(next_name), strength, from_index))
			counts[strength] += 1
		else:
			pulses.append((-1, strength, from_index))
			counts[strength] += 1

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

		if module_index == -1:
			continue

		if curr_module[0][0] == '%' and pulse_strength == 0:
			flip_flop_val[module_index] = 1-flip_flop_val[module_index]

		if curr_module[0][0] == '&':
			conjuction_inputs[pulse_name][module_names[curr_pulse[2]]] = pulse_strength

		for next_module_name in curr_module[1]:
			match curr_module[0][0]:
				case '%':
					if pulse_strength == 0:
						append_to_pulses(next_module_name, flip_flop_val[module_index], module_index, module_names)
				case '&':
					if all(value == 1 for value in conjuction_inputs[pulse_name].values()):
						append_to_pulses(next_module_name, 0, module_index, module_names)
					else:
						append_to_pulses(next_module_name, 1, module_index, module_names)
				case '0':
					append_to_pulses(next_module_name, pulse_strength, module_index, module_names)

# print(flip_flop_val)
for x in range(1000):
	press_button(module_inputs, conjuction_inputs, flip_flop_val)

ans = counts[0]*counts[1]
print(ans)