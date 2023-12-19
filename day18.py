#!/usr/bin/python

"""

--- Day 18: Lavaduct Lagoon ---

Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)

The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######

At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######

Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?

Your puzzle answer was 48795.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

The Elves were right to be concerned; the planned lagoon would be much too small.

After a few minutes, someone realizes what happened; someone swapped the color and instruction parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.

Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

So, in the above example, the hexadecimal codes can be converted into the true instructions:

    #70c710 = R 461937
    #0dc571 = D 56407
    #5713f0 = R 356671
    #d2c081 = D 863240
    #59c680 = R 367720
    #411b91 = D 266681
    #8ceee2 = L 577262
    #caa173 = U 829975
    #1b58a2 = L 112010
    #caa171 = D 829975
    #7807d2 = L 491645
    #a77fa3 = U 686074
    #015232 = L 5411
    #7a21e3 = U 500254

Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115 cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan, how many cubic meters of lava could the lagoon hold?


"""

from collections import deque

def print_shape(pts):
	for y in range(min(pt[1] for pt in pts),max(pt[1] for pt in pts)+1):
		for x in range(min(pt[0] for pt in pts),max(pt[0] for pt in pts)+1):
			if (x,y) in pts:
				print('#',end='')
			else:
				print('.',end='')
		print()

def count_shape(pts):
	total = 0
	for y in range(min(pt[1] for pt in pts),max(pt[1] for pt in pts)+1):
		xs = sorted({ pt[0] for pt in pts if pt[1] == y })
		print(xs)
		while len(xs) > 1:
			total += xs[1] - xs[0]
			xs.pop(0)
			xs.pop(0)
	return total

def cross(a,b):
	return a[0]*b[1] - a[1]*b[0]

def shoelace(pts):
	values = pts[:]
	total = 0
	while len(values) > 1:
		total += cross(values[0],values[1])
		values.pop(0)
	return total//2

def build_shape(instructions):
	deltas = {	'D' : (0,1),
				'L' : (-1,0),
				'R' : (1,0),
				'U' : (0,-1) }
	shape = list()
	pos = (0,0)
	shape.append(pos)
	for d,l,c in instructions:
		for i in range(int(l)+1):
			nx,ny = pos[0]+deltas[d][0]*i,pos[1]+deltas[d][1]*i
			shape.append((nx,ny))
		pos = (nx,ny)
	return shape

def build_shape2(instructions):
	deltas = {	'1' : (0,1),
				'2' : (-1,0),
				'0' : (1,0),
				'3' : (0,-1) }
	shape = list()
	pos = (0,0)
	shape.append(pos)
	per = 0
	for d,t,c in instructions:
		l = int(c[2:-2],16)
		per += l
		d = c[-2]
		nx,ny = pos[0]+deltas[d][0]*int(l),pos[1]+deltas[d][1]*int(l)
		shape.append((nx,ny))
		pos = (nx,ny)
	return shoelace(shape)+per//2 + 1


if __name__ == "__main__":

	# Part 1 Solution
	with open("day18_input", "r") as infile:
		instructions = [ x.split() for x in infile.read().strip().split('\n') ]
	shape = build_shape(instructions)
	shape = set(shape)
	pt = (1,1)
	q = deque()
	q.append(pt)
	shape.add(pt)
	while q:
		pt = q.popleft()
		x,y = pt
		for dx,dy in ((0,1),(1,0),(-1,0),(0,-1)):
			if (x+dx,y+dy) not in shape:
				shape.add((x+dx,y+dy))
				q.append((x+dx,y+dy))

	print(len(shape))


	# Part 2 Solution

	with open("day18_input", "r") as infile:
		instructions = [ x.split() for x in infile.read().strip().split('\n') ]
	print(build_shape2(instructions))
