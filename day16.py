#!/usr/bin/python

"""
--- Day 16: The Floor Will Be Lava ---

With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....

The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

    If the beam encounters empty space (.), it continues in the same direction.
    If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
    If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
    If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.

Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..

Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..

Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?

Your puzzle answer was 7496.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..

Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..

Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?

Your puzzle answer was 7932.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

from collections import deque

layout = dict()

def show_map(s,x_dim,y_dim):
	for y in range(y_dim):
		for x in range(x_dim):
			if (x,y) in s:
				print('#',end='')
			else:
				print('.',end='')
		print()

def beam_walk(x_dim,y_dim,p,d):
	seen = set()
	q = deque()
	seen.add((p,d))
	q.append((p,d))
	while q:
		p,d = q.popleft()
		x,y   = p
		dx,dy = d
		if p not in layout and ((x+dx,y+dy),d) not in seen and x+dx >= 0 and x+dx < x_dim and y+dy >= 0 and y+dy < y_dim:
			seen.add(((x+dx,y+dy),d))
			q.append(((x+dx,y+dy),d))
		elif p in layout:
			m = layout[p]
			if m == '-' and d in ((1,0),(-1,0)): # horizontal travel,no split
				if ((x+dx,y+dy),d) not in seen and x+dx >= 0 and x+dx < x_dim and y+dy >= 0 and y+dy < y_dim:
					seen.add(((x+dx,y+dy),d))
					q.append(((x+dx,y+dy),d))
			elif m == '-' and d in ((0,1),(0,-1)): # vertical travel, split
				for dx,dy in ((1,0),(-1,0)):
					if ((x+dx,y+dy),(dx,dy)) not in seen and x+dx >= 0 and x+dx < x_dim and y+dy >= 0 and y+dy < y_dim:
						seen.add(((x+dx,y+dy),(dx,dy)))
						q.append(((x+dx,y+dy),(dx,dy)))
			elif m == '|' and d in ((0,1),(0,-1)): # vertical travel,no split
				if ((x+dx,y+dy),d) not in seen and x+dx >= 0 and x+dx < x_dim and y+dy >= 0 and y+dy < y_dim:
					seen.add(((x+dx,y+dy),d))
					q.append(((x+dx,y+dy),d))
			elif m == '|' and d in ((1,0),(-1,0)): # horizontal travel, split
				for dx,dy in ((0,1),(0,-1)):
					if ((x+dx,y+dy),(dx,dy)) not in seen and x+dx >= 0 and x+dx < x_dim and y+dy >= 0 and y+dy < y_dim:
						seen.add(((x+dx,y+dy),(dx,dy)))
						q.append(((x+dx,y+dy),(dx,dy)))
			elif m == '/': # 90 degree turn
				if d == (1,0):
					dx,dy = (0,-1) # right to up
				if d == (-1,0):
					dx,dy = (0,1) # left to down
				if d == (0,1):
					dx,dy = (-1,0) # down to left
				if d == (0,-1):
					dx,dy = (1,0) # up to right
				if ((x+dx,y+dy),(dx,dy)) not in seen and x+dx >= 0 and x+dx < x_dim and y+dy >= 0 and y+dy < y_dim:
					seen.add(((x+dx,y+dy),(dx,dy)))
					q.append(((x+dx,y+dy),(dx,dy)))
			elif m == chr(92): # 90 degree turn \
				if d == (1,0):
					dx,dy = (0,1) # right to down
				if d == (-1,0):
					dx,dy = (0,-1) # left to up
				if d == (0,1):
					dx,dy = (1,0) # down to right
				if d == (0,-1):
					dx,dy = (-1,0) # up to left
				if ((x+dx,y+dy),(dx,dy)) not in seen and x+dx >= 0 and x+dx < x_dim and y+dy >= 0 and y+dy < y_dim:
					seen.add(((x+dx,y+dy),(dx,dy)))
					q.append(((x+dx,y+dy),(dx,dy)))
	return { x[0] for x in seen }

if __name__ == "__main__":

	# Part 1 Solution
	with open("day16_input", "r") as infile:
		y = 0
		for line in infile:
			x_dim = len(line.strip())
			for x,c in enumerate(line.strip()):
				if c != '.':
					layout[(x,y)] = c
			y += 1

	energized = beam_walk(x_dim,y,(0,0),(1,0))
	print(len((energized)))

	# Part 2 Solution
	most = 0
	for x in range(x_dim):
		most = max(most,len(beam_walk(x_dim,y,(x,0),(0,1)))) # top row
		most = max(most,len(beam_walk(x_dim,y,(x,y-1),(0,-1)))) # bottom row
	for y in range(y):
		most = max(most,len(beam_walk(x_dim,y,(0,y),(1,0)))) # left
		most = max(most,len(beam_walk(x_dim,y,(x_dim-1,y),(-1,0)))) # right
	# corners
	#most = max(most,len(beam_walk(x_dim,y,(0,0),(0,1))))
	most = max(most,len(beam_walk(x_dim,y,(0,0),(1,0))))
	
	#most = max(most,len(beam_walk(x_dim,y,(x_dim-1,0),(-1,0))))
	most = max(most,len(beam_walk(x_dim,y,(x_dim-1,0),(0,1))))
	
	#most = max(most,len(beam_walk(x_dim,y,(0,y-1),(1,0))))
	most = max(most,len(beam_walk(x_dim,y,(0,y-1),(0,-1))))

	#most = max(most,len(beam_walk(x_dim,y,(x_dim-1,y-1),(-1,0))))
	most = max(most,len(beam_walk(x_dim,y,(x_dim-1,y-1),(0,-1))))
	print(most)
