#!/usr/bin/python

"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

Your puzzle answer was 551094.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

Your puzzle answer was 80179647.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

from collections import deque
import math

digits = '0123456789'

engine_map = dict()
gear_map   = dict()

def symbol_adjacent(x,y):
	q = deque()
	pos = (x,y)
	seen = set()
	seen.add(pos)
	q.append(pos)
	while q:
		pos = q.popleft()
		if pos in engine_map and engine_map[pos] not in digits:
			return True
		x,y = pos
		for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(-1,1),(1,-1)):
			nx,ny = x+dx,y+dy
			if (nx,ny) in engine_map and (nx,ny) not in seen:
				q.append((nx,ny))
				seen.add((nx,ny))
	return False

def gears_adjacent(x,y):
	q = deque()
	pos = (x,y)
	seen = set()
	seen.add(pos)
	q.append(pos)
	touching_pos = []
	while q:
		pos = q.popleft()
		if pos in gear_map:
			touching_pos.append(pos)
		x,y = pos
		for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(-1,1),(1,-1)):
			nx,ny = x+dx,y+dy
			if (nx,ny) in engine_map and (nx,ny) not in seen and engine_map[(nx,ny)] in digits+'*':
				q.append((nx,ny))
				seen.add((nx,ny))
	return touching_pos

if __name__ == "__main__":

	map_x_dim = 0
	map_y_dim = 0

	# Part 1 Solution
	with open("day03_input", "r") as infile:
		y = 0
		for line in infile:
			map_x_dim = len(line)
			for idx,char in enumerate(line.strip()):
				if char != '.':
					engine_map[(idx,y)] = char
				if char == '*':
					gear_map[(idx,y)] = []
			y += 1
		map_y_dim = y

	total = 0
	for y in range(map_y_dim):
		x = 0
		while x < map_x_dim:
			if (x,y) in engine_map and engine_map[(x,y)] in digits and symbol_adjacent(x,y):
				built = ''
				while (x,y) in engine_map and engine_map[(x,y)] in digits:
					built += engine_map[(x,y)]
					x += 1
				total += int(built)
			x += 1
	print(total)

	# Part 2 Solution

	for y in range(map_y_dim):
		x = 0
		while x < map_x_dim:
			if (x,y) in engine_map and engine_map[(x,y)] in digits:
				gear_adj_list = gears_adjacent(x,y)
				if len(gear_adj_list) == 1:
					built = ''
					while (x,y) in engine_map and engine_map[(x,y)] in digits:
						built += engine_map[(x,y)]
						x += 1
					gear_map[gear_adj_list[0]].append(int(built))
			x += 1

	print(sum(math.prod(e) for e in gear_map.values() if len(e) == 2))
