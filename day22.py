#!/usr/bin/python

"""
--- Day 22: Sand Slabs ---
Enough sand has fallen; it can finally filter water for Snow Island.

Well, almost.

The sand has been falling as large compacted bricks of sand, piling up to form an impressive stack here near the edge of Island Island. In order to make use of the sand to filter water, some of the bricks will need to be broken apart - nay, disintegrated - back into freely flowing sand.

The stack is tall enough that you'll have to be careful about choosing which bricks to disintegrate; if you disintegrate the wrong brick, large portions of the stack could topple, which sounds pretty dangerous.

The Elves responsible for water filtering operations took a snapshot of the bricks while they were still falling (your puzzle input) which should let you work out which bricks are safe to disintegrate. For example:

1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
Each line of text in the snapshot represents the position of a single brick at the time the snapshot was taken. The position is given as two x,y,z coordinates - one for each end of the brick - separated by a tilde (~). Each brick is made up of a single straight line of cubes, and the Elves were even careful to choose a time for the snapshot that had all of the free-falling bricks at integer positions above the ground, so the whole snapshot is aligned to a three-dimensional cube grid.

A line like 2,2,2~2,2,2 means that both ends of the brick are at the same coordinate - in other words, that the brick is a single cube.

Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks that are two cubes in volume, both oriented horizontally. The first brick extends in the x direction, while the second brick extends in the y direction.

A line like 0,0,1~0,0,10 represents a ten-cube brick which is oriented vertically. One end of the brick is the cube located at 0,0,1, while the other end of the brick is located directly above it at 0,0,10.

The ground is at z=0 and is perfectly flat; the lowest z value a brick can have is therefore 1. So, 5,5,1~5,6,1 and 0,2,1~0,2,5 are both resting on the ground, but 3,3,2~3,3,3 was above the ground at the time of the snapshot.

Because the snapshot was taken while the bricks were still falling, some bricks will still be in the air; you'll need to start by figuring out where they will end up. Bricks are magically stabilized, so they never rotate, even in weird situations like where a long horizontal brick is only supported on one end. Two bricks cannot occupy the same position, so a falling brick will come to rest upon the first other brick it encounters.

Here is the same example again, this time with each brick given a letter so it can be marked in diagrams:

1,0,1~1,2,1   <- A
0,0,2~2,0,2   <- B
0,2,3~2,2,3   <- C
0,0,4~0,2,4   <- D
2,0,5~2,2,5   <- E
0,1,6~2,1,6   <- F
1,1,8~1,1,9   <- G
At the time of the snapshot, from the side so the x axis goes left to right, these bricks are arranged like this:

 x
012
.G. 9
.G. 8
... 7
FFF 6
..E 5 z
D.. 4
CCC 3
BBB 2
.A. 1
--- 0
Rotating the perspective 90 degrees so the y axis now goes left to right, the same bricks are arranged like this:

 y
012
.G. 9
.G. 8
... 7
.F. 6
EEE 5 z
DDD 4
..C 3
B.. 2
AAA 1
--- 0
Once all of the bricks fall downward as far as they can go, the stack looks like this, where ? means bricks are hidden behind other bricks at that location:

 x
012
.G. 6
.G. 5
FFF 4
D.E 3 z
??? 2
.A. 1
--- 0
Again from the side:

 y
012
.G. 6
.G. 5
.F. 4
??? 3 z
B.C 2
AAA 1
--- 0
Now that all of the bricks have settled, it becomes easier to tell which bricks are supporting which other bricks:

Brick A is the only brick supporting bricks B and C.
Brick B is one of two bricks supporting brick D and brick E.
Brick C is the other brick supporting brick D and brick E.
Brick D supports brick F.
Brick E also supports brick F.
Brick F supports brick G.
Brick G isn't supporting any bricks.
Your first task is to figure out which bricks are safe to disintegrate. A brick can be safely disintegrated if, after removing it, no other bricks would fall further directly downward. Don't actually disintegrate any bricks - just determine what would happen if, for each brick, only that brick were disintegrated. Bricks can be disintegrated even if they're completely surrounded by other bricks; you can squeeze between bricks if you need to.

In this example, the bricks can be disintegrated as follows:

Brick A cannot be disintegrated safely; if it were disintegrated, bricks B and C would both fall.
Brick B can be disintegrated; the bricks above it (D and E) would still be supported by brick C.
Brick C can be disintegrated; the bricks above it (D and E) would still be supported by brick B.
Brick D can be disintegrated; the brick above it (F) would still be supported by brick E.
Brick E can be disintegrated; the brick above it (F) would still be supported by brick D.
Brick F cannot be disintegrated; the brick above it (G) would fall.
Brick G can be disintegrated; it does not support any other bricks.
So, in this example, 5 bricks can be safely disintegrated.

Figure how the blocks will settle based on the snapshot. Once they've settled, consider disintegrating a single brick; how many bricks could be safely chosen as the one to get disintegrated?

Your puzzle answer was 515.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Disintegrating bricks one at a time isn't going to be fast enough. While it might sound dangerous, what you really need is a chain reaction.

You'll need to figure out the best brick to disintegrate. For each brick, determine how many other bricks would fall if that brick were disintegrated.

Using the same example as above:

    Disintegrating brick A would cause all 6 other bricks to fall.
    Disintegrating brick F would cause only 1 other brick, G, to fall.

Disintegrating any other brick would cause no other bricks to fall. So, in this example, the sum of the number of other bricks that would fall as a result of disintegrating each brick is 7.

For each brick, determine how many other bricks would fall if that brick were disintegrated. What is the sum of the number of other bricks that would fall?

Your puzzle answer was 101541.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

import copy

class Brick:
	
	def __init__(self, init_string=None):
		self.volume = set()
		self.fell  = False
		if init_string == None:
			return
		a,b = init_string.split('~')
		x1,y1,z1 = (int(x) for x in a.split(','))
		x2,y2,z2 = (int(x) for x in b.split(','))
		for z in range(min(z1,z2),max(z1,z2)+1):
			for y in range(min(y1,y2),max(y1,y2)+1):
				for x in range(min(x1,x2),max(x1,x2)+1):
					self.volume.add((x,y,z))

	def footprint_bounds(self):
		x_min = min( t[0] for t in self.volume )
		x_max = max( t[0] for t in self.volume ) + 1
		y_min = min( t[1] for t in self.volume )
		y_max = max( t[1] for t in self.volume ) + 1
		return ((x_min,y_min),(x_max,y_max))

	def footprint(self):
		return { (x,y) for x,y,z in self.volume }

	def ceiling(self):
		return max( t[2] for t in self.volume )
	
	def floor(self):
		return min( t[2] for t in self.volume )

	# move the brick as low as possible by looking at any bricks below this one
	def drop(self,other_bricks):
		if 1 in { t[2] for t in self.volume }:
			return False
		other_bricks = [ b for b in other_bricks if b != self ]
		footy = self.footprint()
		other_bricks = [ b for b in other_bricks if len(footy.intersection(b.footprint())) > 0 ]
		collision_volume = set()
		for b in other_bricks:
			for e in b.volume:
				collision_volume.add(e)
		moved = False
		while 1 not in { t[2] for t in self.volume }:
			new_volume = { (x,y,z-1) for x,y,z in self.volume }
			if len(new_volume.intersection(collision_volume)) == 0:
				moved = True
				self.fell = True
				self.volume = new_volume
			else:
				return moved
		return moved

	# determine if it is possible to move a block down by 1 square
	def bump(self,global_volume):
		if 1 in { t[2] for t in self.volume }:
			return False
		for e in self.volume:
			global_volume.discard(e)
		new_volume = { (x,y,z-1) for x,y,z in self.volume }
		if len(new_volume.intersection(global_volume)) == 0:
			return True
		return False

	# move the brick down one square if possible
	def bump2(self,other_bricks):
		if 1 in { t[2] for t in self.volume }:
			return
		other_bricks = [ b for b in other_bricks if b != self ]
		footy = self.footprint()
		other_bricks = [ b for b in other_bricks if len(footy.intersection(b.footprint())) > 0 ]
		collision_volume = set()
		for b in other_bricks:
			for e in b.volume:
				collision_volume.add(e)
		new_volume = { (x,y,z-1) for x,y,z in self.volume }
		if len(new_volume.intersection(collision_volume)) == 0:
			self.fell = True
			self.volume = new_volume

if __name__ == "__main__":

	bricks = []
	# Part 1 Solution
	with open("day22_input", "r") as infile:
		for line in infile:
			b = Brick(line.strip())
			bricks.append(b)

	# compress stack
	for i in range(1,max( b.ceiling() for b in bricks)):
		chunk = [ b for b in bricks if i in { t[2] for t in b.volume } ]
		while any( b.drop(bricks) for b in chunk ):
			continue

	global_volume = set()
	for b in bricks:
		for e in b.volume:
			global_volume.add(e)

	brick_count = 0
	excludes = set()
	for i in range(len(bricks)):
		current_volume = { x for x in global_volume }
		trial_stack = [ copy.copy(b) for b in bricks ]
		removed = trial_stack.pop(i)
		for e in removed.volume:
			current_volume.discard(e)
		if not any( b.bump(copy.copy(current_volume)) for b in trial_stack ):
			brick_count += 1
			excludes.add(i)
	print(brick_count)

	# Part 2 Solution

	brick_count = 0
	for j in range(len(bricks)):
		if j not in excludes:
			trial_stack = [ copy.copy(b) for b in bricks ]
			for b in trial_stack:
				b.fell = False
			removed = trial_stack.pop(j)
			# compress stack, but only by 1 movement per brick
			for i in range(1,max( b.ceiling() for b in trial_stack )):
				chunk = [ b for b in trial_stack if i in { t[2] for t in b.volume } and not b.fell ]
				[ b.bump2(trial_stack) for b in chunk ]
			brick_count += sum( b.fell for b in trial_stack )
	print(brick_count)
