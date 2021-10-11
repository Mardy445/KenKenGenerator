import random
from block import Block

"""
This file contains the code to randomly segment a sz*sz square into a number of Blocks 
This is used as an alternative to kenken_generation.py
By randomly generating the grid, there may be no logically achievable solution
A game generated by this file could be solved with backtracking, 
but that is not how humans should need to think when playing a real game of KenKen
"""


class RandomGridSegmentation:
    available_positions = []
    blocks = []

    def __init__(self, sz, number_grid):
        self.sz = sz
        self.number_grid = number_grid
        self.available_positions = []
        for x in range(self.sz):
            for y in range(self.sz):
                self.available_positions.append((x, y))
        random.shuffle(self.available_positions)
        self.blocks = []

    """
    Randomly generates a list of blocks such that every position in a sz*sz square is used
    """

    def randomly_segment_grid(self):
        while len(self.available_positions) > 0:
            # Pops a position as the initial tile in a block
            block_init_pos = self.available_positions.pop()
            block = Block(block_init_pos, self.number_grid[block_init_pos[0]][block_init_pos[1]],self.sz)
            self.blocks.append(block)
            while True:
                r = random.uniform(0, 1)
                f = (1 / (len(block.positions) + 0.01))

                # Uses random number generation to determine whether or not to attempt to add another tile
                if r > f or len(block.positions) == self.sz:
                    break
                pos = block.get_possible_next_position(self.available_positions)
                # If no possible neighbours, end generation for this block
                if pos is None:
                    break
                else:
                    self.available_positions.remove(pos)
                    block.add_new_tile(pos, self.number_grid[pos[0]][pos[1]])

            if len(block.positions) == 1:
                block.value = self.number_grid[block_init_pos[0]][block_init_pos[1]]
            else:
                signs = ["/", "-", "+", "*"]
                random.shuffle(signs)
                for sign in signs:
                    if sign == "+":
                        block.calculate_plus(self.number_grid)
                    elif sign == "-":
                        block.calculate_minus(self.number_grid)
                    elif sign == "*":
                        block.calculate_multiply(self.number_grid)
                    elif sign == "/":
                        block.calculate_divide(self.number_grid)
                    if block.sign is not None:
                        break
        return self.blocks