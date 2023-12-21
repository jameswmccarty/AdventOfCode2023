#!/usr/bin/python

"""
--- Day 20: Pulse Propagation ---

With your help, the Elves manage to find the right parts and fix all of the machines. Now, they just need to send the command to boot up the machines and get the sand flowing again.

The machines are far apart and wired together with long cables. The cables don't connect to the machines directly, but rather to communication modules attached to the machines that perform various initialization tasks and also act as communication relays.

Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. When a module sends a pulse, it sends that type of pulse to each module in its list of destination modules.

There are several different types of modules:

Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.

Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module. When you push the button, a single low pulse is sent directly to the broadcaster module.

After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it again. Never push the button if modules are still processing pulses.

Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a, b, and c, and then module a processes its pulse and sends more pulses, the pulses sent to modules b and c would have to be handled first.

The module configuration (your puzzle input) lists each module. The name of the module is preceded by a symbol identifying its type, if any. The name is then followed by an arrow and a list of its destination modules. For example:

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a

In this module configuration, the broadcaster has three destination modules named a, b, and c. Each of these modules is a flip-flop module (as indicated by the % prefix). a outputs to b which outputs to c which outputs to another module named inv. inv is a conjunction module (as indicated by the & prefix) which, because it has only one input, acts like an inverter (it sends the opposite of the pulse type it receives); it outputs to a.

By pushing the button once, the following pulses are sent:

button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a

After this sequence, the flip-flop modules all end up off, so pushing the button again repeats the same sequence.

Here's a more interesting example:

broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output

This module configuration includes the broadcaster, two flip-flops (named a and b), a single-input conjunction module (inv), a multi-input conjunction module (con), and an untyped module named output (for testing purposes). The multi-input conjunction module con watches the two flip-flop modules and, if they're both on, sends a low pulse to the output module.

Here's what happens if you push the button once:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output

Both flip-flops turn on and a low pulse is sent to output! However, now that both flip-flops are on and con remembers a high pulse from each of its two inputs, pushing the button a second time does something different:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output

Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high pulse to output.

Push the button a third time:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output

This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off, the pulse sent to con is handled first, so it briefly remembers all high pulses for its inputs and sends a low pulse to output. After that, flip-flop b turns off, which causes con to update its state and send a high pulse to output.

Finally, with a on and b off, push the button a fourth time:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output

This completes the cycle: a turns off, causing con to remember only low pulses and restoring all modules to their original states.

To get the cables warmed up, the Elves have pushed the button 1000 times. How many pulses got sent as a result (including the pulses sent by the button itself)?

In the first example, the same thing happens every time the button is pushed: 8 low pulses and 4 high pulses are sent. So, after pushing the button 1000 times, 8000 low pulses and 4000 high pulses are sent. Multiplying these together gives 32000000.

In the second example, after pushing the button 1000 times, 4250 low pulses and 2750 high pulses are sent. Multiplying these together gives 11687500.

Consult your module configuration; determine the number of low pulses and high pulses that would be sent after pushing the button 1000 times, waiting for all pulses to be fully handled after each push of the button. What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?

Your puzzle answer was 777666211.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

The final machine responsible for moving the sand down to Island Island has a module attached named rx. The machine turns on when a single low pulse is sent to rx.

Reset all modules to their default states. Waiting for all pulses to be fully handled after each button press, what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

"""

from collections import deque

high_sent = 0
low_sent  = 0

class Button:

	def __init__(self,output):
		self.name = 'button'
		self.output = None

	def get_name(self):
		return self.name

	def add_output(self,module):
		self.output = module

	def kind(self):
		return 'button'

	def tick(self):
		return False

	def press(self):
		global low_sent
		#print(self.get_name(), "Sent a pulse")
		low_sent += 1
		self.output.recv('-low',self)

class Output:

	def __init__(self,a):
		self.name = a
		self.low_count = 0
		self.high_count = 0

	def get_name(self):
		return self.name

	def kind(self):
		return self.name

	def tick(self):
		return False

	def recv(self,pulse,source):
		global low_sent,high_sent
		if pulse == '-low':
			self.low_count += 1
		if pulse == '-high':
			self.high_count += 1
		#print("Outputs are now: ",self.low_count,"-low and",self.high_count,"-high pulses")
		#print("Global counts are",low_sent,high_sent)

class Broadcaster:

	def __init__(self):
		self.name = 'broadcaster'
		self.outputs = []
		self.signal_line = deque()

	def get_name(self):
		return self.name

	def kind(self):
		return 'broadcaster'

	def add_output(self,module):
		self.outputs.append(module)

	def tick(self):
		global low_sent,high_sent
		if self.signal_line:
			pulse = self.signal_line.popleft()
			for e in self.outputs:
				#print(self.get_name(), "Sent a pulse to ",e.get_name())
				e.recv(pulse,self)
				if pulse == '-low':
					low_sent += 1
				else:
					high_sent += 1
			return True
		return False

	def recv(self,pulse,source):
		self.signal_line.append(pulse)

class FlipFlop:

	def __init__(self,name):
		self.name = name[1:]
		self.outputs = []
		self.state = False
		self.signal_line = deque()

	def kind(self):
		return 'flipflop'

	def get_name(self):
		return self.name

	def add_output(self,module):
		self.outputs.append(module)

	def tick(self):
		global low_sent,high_sent
		if self.signal_line:
			pulse = self.signal_line.popleft()
			if pulse == '-low':
				self.state ^= True
				if self.state:
					for e in self.outputs:
						e.recv('-high',self)
						high_sent += 1
				else:
					for e in self.outputs:
						low_sent += 1
						e.recv('-low',self)
			return True
		return False

	def recv(self,pulse,source):
		#print(self.get_name(), "Got a pulse from",source.get_name())
		self.signal_line.append(pulse)

class Conjunction:

	def __init__(self,name):
		self.name = name[1:]
		self.outputs = []
		self.inputs  = dict()
		self.signal_line = deque()

	def get_name(self):
		return self.name

	def kind(self):
		return 'conjunction'

	def add_output(self,module):
		self.outputs.append(module)

	def add_input(self,module):
		self.inputs[module] = '-low'

	def tick(self):
		global low_sent,high_sent
		if all( value == '-high' for value in self.inputs.values() ):
			for e in self.outputs:
				e.recv('-low',self)
				low_sent += 1
		else:
			for e in self.outputs:
				e.recv('-high',self)
				high_sent += 1
		return False

	def recv(self,pulse,source):
		self.inputs[source] = pulse
		self.tick()

def gen_module_pass1(line):
	source,dest = line.strip().split(' -> ')
	if source == 'button':
		return Button(dest.strip())
	if source == 'broadcaster':
		return Broadcaster()
	if source == 'output':
		return Output()
	if '%' in source:
		return FlipFlop(source)
	if '&' in source:
		return Conjunction(source)
	return None


if __name__ == "__main__":

	Modules = dict()

	# Part 1 Solution
	with open("day20_input", "r") as infile:
		for line in infile:
			module = gen_module_pass1(line)
			Modules[module.get_name()] = module

	#if 'output' not in Modules:
	#	Modules['output'] = Output('output')

	with open("day20_input", "r") as infile:
		for line in infile:
			source,dest = line.strip().split(' -> ')
			for entry in dest.split(', '):
				if entry not in Modules:
					Modules[entry] = Output(entry)
			if source == 'broadcaster':
				for entry in dest.split(', '):
					Modules[source].add_output(Modules[entry])
			if source == 'button':
				for entry in dest.split(', '):
					Modules[source].add_output(Modules[entry])
			if '%' in source:
				for entry in dest.split(', '):
					Modules[source[1:]].add_output(Modules[entry])
			if '&' in source:
				for entry in dest.split(', '):
					Modules[source[1:]].add_output(Modules[entry])
			for entry in dest.split(', '):
				if Modules[entry].kind() == 'conjunction':
					source_name = source[1:] if '%' in source or '&' in source else source
					Modules[entry].add_input(Modules[source_name])

	for _ in range(1000):
		Modules['button'].press()
		while any( v.tick() if v.kind() != 'conjunction' else False for k,v in Modules.items() ):
			continue

	print(low_sent*high_sent)

	# Part 2 Solution

