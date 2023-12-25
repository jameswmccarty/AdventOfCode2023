#!/usr/bin/python

"""
--- Day 25: Snowverload ---
Still somehow without snow, you go to the last place you haven't checked: the center of Snow Island, directly below the waterfall.

Here, someone has clearly been trying to fix the problem. Scattered everywhere are hundreds of weather machines, almanacs, communication modules, hoof prints, machine parts, mirrors, lenses, and so on.

Somehow, everything has been wired together into a massive snow-producing apparatus, but nothing seems to be running. You check a tiny screen on one of the communication modules: Error 2023. It doesn't say what Error 2023 means, but it does have the phone number for a support line printed on it.

"Hi, you've reached Weather Machines And So On, Inc. How can I help you?" You explain the situation.

"Error 2023, you say? Why, that's a power overload error, of course! It means you have too many components plugged in. Try unplugging some components and--" You explain that there are hundreds of components here and you're in a bit of a hurry.

"Well, let's see how bad it is; do you see a big red reset button somewhere? It should be on its own module. If you push it, it probably won't fix anything, but it'll report how overloaded things are." After a minute or two, you find the reset button; it's so big that it takes two hands just to get enough leverage to push it. Its screen then displays:

SYSTEM OVERLOAD!

Connected components would require
power equal to at least 100 stars!
"Wait, how many components did you say are plugged in? With that much equipment, you could produce snow for an entire--" You disconnect the call.

You have nowhere near that many stars - you need to find a way to disconnect at least half of the equipment here, but it's already Christmas! You only have time to disconnect three wires.

Fortunately, someone left a wiring diagram (your puzzle input) that shows how the components are connected. For example:

jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
Each line shows the name of a component, a colon, and then a list of other components to which that component is connected. Connections aren't directional; abc: xyz and xyz: abc both represent the same configuration. Each connection between two components is represented only once, so some components might only ever appear on the left or right side of a colon.

In this example, if you disconnect the wire between hfx/pzl, the wire between bvb/cmg, and the wire between nvd/jqt, you will divide the components into two separate, disconnected groups:

9 components: cmg, frs, lhk, lsr, nvd, pzl, qnr, rsh, and rzs.
6 components: bvb, hfx, jqt, ntq, rhn, and xhk.
Multiplying the sizes of these groups together produces 54.

Find the three wires you need to disconnect in order to divide the components into two separate groups. What do you get if you multiply the sizes of these two groups together?

Your puzzle answer was 507626.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
You climb over weather machines, under giant springs, and narrowly avoid a pile of pipes as you find and disconnect the three wires.

A moment after you disconnect the last wire, the big red reset button module makes a small ding noise:

System overload resolved!
Power required is now 50 stars.
Out of the corner of your eye, you notice goggles and a loose-fitting hard hat peeking at you from behind an ultra crucible. You think you see a faint glow, but before you can investigate, you hear another small ding:

Power required is now 49 stars.

Please supply the necessary stars and
push the button to restart the system.

"""

import graphviz
from collections import deque

class Node:

	def __init__(self,name):
		self.name = name
		self.connections = set()


def bfs(node,nodes):
	seen = set()
	q = deque()
	q.append(node)
	seen.add(node)
	while q:
		current = q.popleft()
		for edge in nodes[current]:
			if edge not in seen:
				seen.add(edge)
				q.append(edge)
	return len(seen)

cut_candidates = set()
def bfs2(node,nodes):
	seen = set()
	dist_map = dict()
	q = deque()
	q.append((node,0))
	seen.add(node)
	while q:
		current,dist = q.popleft()
		for edge in nodes[current]:
			if dist not in dist_map:
				dist_map[dist] = list()
			if edge not in seen:
				seen.add(edge)
				q.append((edge,dist+1))
				t = (current,edge)
				dist_map[dist].append('-'.join(sorted(t)))
	for dist in dist_map:
		if len(dist_map[dist]) == 3:
			unique = set()
			for entry in dist_map[dist]:
				for item in entry.split('-'):
					unique.add(item)
			if len(unique) == 6:
				cut_candidates.add(','.join(sorted(dist_map[dist])))

if __name__ == "__main__":

	nodes = dict()
	connections = list()
	seen = set()

	f = graphviz.Digraph(filename = "day25_graph.gv")

	# Part 1 Solution
	with open("day25_input", "r") as infile:
		for line in infile:
			connections.append(line.strip())
			line = line.strip().replace(":",'')
			for item in line.split():
				if item not in seen:
					seen.add(item)
					f.node(item,item)
					nodes[item] = set()

	for line in connections:
		source,dests = line.split(":")
		for entry in dests.split():
			if not (entry in nodes[source] or source in nodes[entry]):
				f.edge(entry,source)
				nodes[source].add(entry)
				nodes[entry].add(source)


	# Manually determine the links to cut
	
	#f.view()
	
	#kbr-bbg	
	#fht-vtt
	#tdk-czs
	
	#nodes['hfx'].discard('pzl')
	#nodes['pzl'].discard('hfx')
	#nodes['bvb'].discard('cmg')
	#nodes['cmg'].discard('bvb')
	#nodes['nvd'].discard('jqt')
	#nodes['jqt'].discard('nvd')
	
	for node in nodes:
		bfs2(node,nodes)

	for trial in cut_candidates:
		nodes = dict()
		connections = list()
		seen = set()
		with open("day25_input", "r") as infile:
			for line in infile:
				connections.append(line.strip())
				line = line.strip().replace(":",'')
				for item in line.split():
					if item not in seen:
						seen.add(item)
						nodes[item] = set()

		for line in connections:
			source,dests = line.split(":")
			for entry in dests.split():
				if not (entry in nodes[source] or source in nodes[entry]):
					nodes[source].add(entry)
					nodes[entry].add(source)




		a,b,c = trial.split(',')
		a1,a2 = a.split('-')
		b1,b2 = b.split('-')
		c1,c2 = c.split('-')
		nodes[a1].discard(a2)
		nodes[a2].discard(a1)
		nodes[b1].discard(b2)
		nodes[b2].discard(b1)
		nodes[c1].discard(c2)
		nodes[c2].discard(c1)
	
		g1,g2 = bfs(a1,nodes),bfs(a2,nodes)
		if g1 != g2:
			print(g1*g2)
			exit()


