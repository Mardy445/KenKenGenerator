import random
import tkinter
from block import Block

"""
This file contains the code to randomly segment a sz*sz square into a number of Blocks 
"""

class RandomGridSegmentation:
    available_positions = []
    blocks = []

    def __init__(self, sz):
        self.sz = sz
        self.reset_variables()

    """
    Resets the variables for grid resegmentation
    """
    def reset_variables(self):
        self.available_positions = []
        for x in range(self.sz):
            for y in range(self.sz):
                self.available_positions.append((x, y))
        random.shuffle(self.available_positions)
        self.blocks = []

    """
    Randomly generates a list of blocks such that every position in a sz*sz square is used
    """
    def segment_grid(self):
        self.reset_variables()
        while len(self.available_positions) > 0:
            # Pops a position as the initial tile in a block
            block_init_pos = self.available_positions.pop()
            block = Block(block_init_pos, self.sz)
            self.blocks.append(block)
            while True:
                r = random.uniform(0, 1)
                f = (1 / (len(block.positions)+0.01))

                # Uses random number generation to determine whether or not to attempt to add another tile
                if r > f or len(block.positions) == self.sz:
                    break
                pos = block.get_possible_next_position(self.available_positions)
                # If no possible neighbours, end generation for this block
                if pos is None:
                    break
                else:
                    self.available_positions.remove(pos)
                    block.add_new_tile(pos)
        print(len(self.blocks))

    """
    Method used solely for testing purposes
    """
    def create_printable_form(self):
        grid = []
        hold = [0] * self.sz
        for i in range(self.sz):
            grid.append(hold.copy())
        for i, block in enumerate(self.blocks):
            # print((block.positions))
            for pos in block.positions:
                grid[pos[0]][pos[1]] = i
        return grid


"""
The code below was used for testing solely the grid segmentation functionality
"""
if __name__ == '__main__':
    size = 6

    grid_map = RandomGridSegmentation(size)
    grid_map.segment_grid()
    root = tkinter.Tk()
    gp = grid_map.create_printable_form()
    for c in range(size):
        for r in range(size):
            tkinter.Button(root, width=10, height=5, text=gp[r][c], bg="white").grid(row=r, column=c)
    root.mainloop()
