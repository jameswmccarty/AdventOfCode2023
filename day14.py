#!/usr/bin/python

"""

--- Day 14: Parabolic Reflector Dish ---

You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

Your puzzle answer was 112773.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

Your puzzle answer was 98894.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

moveable_rock_pos = set()

class Rock:

	deltas = { "N" : (0,-1),
			   "S" : (0,1),
			   "E" : (1,0),
			   "W" : (-1,0) }

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.x_dim = None
		self.y_dim = None

	def dims(self,x,y):
		self.x_dim = x
		self.y_dim = y

	def pos(self):
		return (self.x,self.y)

	def move(self,d,cubes):
		global moveable_rock_pos
		dx,dy = self.deltas[d]
		nx,ny = self.x+dx,self.y+dy
		if (nx,ny) not in moveable_rock_pos and (nx,ny) not in cubes and nx >= 0 and ny >= 0 and nx < self.x_dim and ny < self.y_dim:
			while (nx,ny) not in moveable_rock_pos and (nx,ny) not in cubes and nx >= 0 and ny >= 0 and nx < self.x_dim and ny < self.y_dim:
				moveable_rock_pos.discard((self.x,self.y))
				moveable_rock_pos.add((nx,ny))
				self.x,self.y = nx,ny
				nx,ny = nx+dx,ny+dy
			return True
		return False

	def score(self):
		return self.y_dim - self.y


if __name__ == "__main__":

	# Part 1 Solution
	fixed_rocks = set()
	moveable_rocks = set()
	with open("day14_input", "r") as infile:
		y = 0
		for line in infile:
			x_dim = len(line.strip())
			for x,c in enumerate(line.strip()):
				if c == "O":
					moveable_rocks.add(Rock(x,y))
				if c == "#":
					fixed_rocks.add((x,y))
			y += 1

	for e in moveable_rocks:
		e.dims(y,x_dim)

	moveable_rock_pos = { r.pos() for r in moveable_rocks }
	while any( r.move("N",fixed_rocks) for r in moveable_rocks ):
		continue

	print(sum( r.score() for r in moveable_rocks ))

	# Part 2 Solution

	fixed_rocks = set()
	moveable_rocks = set()
	with open("day14_input", "r") as infile:
		y = 0
		for line in infile:
			x_dim = len(line.strip())
			for x,c in enumerate(line.strip()):
				if c == "O":
					moveable_rocks.add(Rock(x,y))
				if c == "#":
					fixed_rocks.add((x,y))
			y += 1

	for e in moveable_rocks:
		e.dims(y,x_dim)

	moveable_rock_pos = { r.pos() for r in moveable_rocks }
	cycles = dict()
	cycles[hash(frozenset(moveable_rock_pos))] = 0
	c = 0
	c_max = 1000000000
	looped = False
	while c < c_max:

		for d in "NWSE":
			while any( r.move(d,fixed_rocks) for r in moveable_rocks ):
				continue
		cycle_set = hash(frozenset(moveable_rock_pos))
		if cycle_set in cycles and not looped:
			#print(cycles[cycle_set],sum( r.score() for r in moveable_rocks ),c)
			cycles[cycle_set].append(c)
			c_max = ( c_max - cycles[cycle_set][0] )  % (cycles[cycle_set][1] - cycles[cycle_set][0])
			looped = True
			c = 0
		else:
			cycles[cycle_set] = [c]
		#print(cycle,sum( r.score() for r in moveable_rocks ))
		c += 1
print(sum( r.score() for r in moveable_rocks ))
