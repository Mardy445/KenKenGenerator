import copy
import random
from block import Block
MAX_ATTEMPTS = 5

"""
This is the main file for generation the grid.
It works by iteratively randomly generating blocks.
Each block generated is checked to see if its addition contributes any useful information to solving the game.
If it does contribute useful information, keep the block, otherwise discard it.
By generating the game this way, it can be certain that a path to a solution exists. 
"""

"""
Generates an initial grid of zeroes
"""
def get_empty_grid_of_zeroes(sz):
    init_grid = []
    hold = [0] * sz
    for i in range(sz):
        init_grid.append(hold.copy())
    return init_grid


"""
Generates an initial grid of lists
"""
def get_empty_grid_of_lists(sz):
    init_reserved_values = []
    hold = []
    for i in range(sz):
        hold.append([])
    for i in range(sz):
        init_reserved_values.append(copy.deepcopy(hold))
    return init_reserved_values


class KenKenGenerationBlockByBlock:
    # Counts how many blocks have been generated since the last block was added
    current_attempts = 0

    def __init__(self, sz, number_grid):
        self.sz = sz
        self.number_grid = number_grid

        init_available_positions = []
        for x in range(self.sz):
            for y in range(self.sz):
                init_available_positions.append((x, y))
        random.shuffle(init_available_positions)

        self.current_grid = get_empty_grid_of_zeroes(sz)
        self.reserved_values_grid_p1 = get_empty_grid_of_lists(sz)
        self.reserved_values_grid_p2 = copy.deepcopy(self.reserved_values_grid_p1)
        self.available_positions = init_available_positions
        self.blocks = []

    """
    The primary iteration function to generate the grid
    """
    def generate_kenken_grid(self):
        # While not every tile exists in a block
        while len(self.available_positions) > 0:
            block = self.generate_random_block(self.available_positions)

            # If the new block is a single tile, then no further calculations are needed,
            # since a single tile block will ALWAYS provide information on its exact value
            if (len(block.positions) == 1):
                block.set_value(self.number_grid[block.positions[0][0]][block.positions[0][1]])
                self.update_all_information_grids(block, [True], [], [])
                continue

            # The signs are checked in this order, from least likely to be provide information to most likely
            # This is done to avoid a grid of mostly multiplication signs to be generated
            signs = ["/", "-", "+", "*"]
            #random.shuffle(signs)
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
                    unique_bool_array, hold_p1_absolutes, hold_p2_absolutes = block.get_block_information(
                        self.current_grid, self.reserved_values_grid_p1, self.reserved_values_grid_p2)
                    # If any of the blocks tiles can be determined, or the block can reserve values for any of the rows or columns,
                    # keep the block
                    if any(unique_bool_array) or len(hold_p1_absolutes) > 0 or len(hold_p2_absolutes) > 0:
                        self.update_all_information_grids(block, unique_bool_array, hold_p1_absolutes, hold_p2_absolutes)
                        self.current_attempts = 0
                        break
                    else:
                        block.reset_value_and_sign()
            self.current_attempts += 1

    def generate_random_block(self, available_positions):
        block_init_pos = available_positions[random.randint(0, len(available_positions) - 1)]
        block = Block(block_init_pos, self.number_grid[block_init_pos[0]][block_init_pos[1]], self.sz)
        # If there have been a certain number of failed attempts, return the single tile block
        if self.current_attempts == MAX_ATTEMPTS:
            self.current_attempts = 0
            return block

        # Otherwise add at least 1 new tile
        # This is done to avoid a grid of mostly single tiles

        r = 0
        f = 1
        while r < f and len(block.positions) < 5:
            pos = block.get_possible_next_position(available_positions)
            # If no possible neighbours, end generation for this block
            if pos is not None:
                block.add_new_tile(pos, self.number_grid[pos[0]][pos[1]])
                r = random.uniform(0, 1)
                f = (1 / (len(block.positions) + 0.01))
            else:
                break
        return block

    """
    Given the new block and its information, update the main grid and the reserved value grids accordingly
    for the new block and all existing blocks
    """
    def update_all_information_grids(self, block, value_array, hold_p1_absolutes, hold_p2_absolutes):
        self.update_values_given_block(block, value_array, hold_p1_absolutes, hold_p2_absolutes)
        for pos in block.positions:
            self.available_positions.remove(pos)

        # Once the new blocks changes are added, check all other existing blocks to see if any new information
        # can be determined
        for hold_block in self.blocks:
            if hold_block.complete:
                continue
            u, p1_a, p2_a = hold_block.get_block_information(self.current_grid, self.reserved_values_grid_p1,
                                                             self.reserved_values_grid_p2)
            self.update_values_given_block(hold_block, u, p1_a, p2_a)

        self.blocks.append(block)

    """
    Updates the main grid and reserved values grids for a given block
    """
    def update_values_given_block(self, block, value_array, hold_p1_absolutes, hold_p2_absolutes):
        if all(value_array):
            block.complete = True
        for i, pos in enumerate(block.positions):
            if value_array[i]:
                self.current_grid[pos[0]][pos[1]] = self.number_grid[pos[0]][pos[1]]
            self.reserved_values_grid_p1[pos[0]][pos[1]].extend(hold_p1_absolutes)
            self.reserved_values_grid_p2[pos[0]][pos[1]].extend(hold_p2_absolutes)
            block.p1_absolutes.extend(hold_p1_absolutes)
            block.p2_absolutes.extend(hold_p2_absolutes)
